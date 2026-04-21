#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / 'scripts'
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import graph  # noqa: E402
import ncu_analysis  # noqa: E402
import state_lib  # noqa: E402
from state_lib import default_benchmark_state  # noqa: E402


FIXTURE_DIR = REPO_ROOT / 'tests' / 'fixtures' / 'ncu'
HEADLINE_METRICS = [
    'sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active',
    'sm__throughput.avg.pct_of_peak_sustained_elapsed',
    'sm__warps_active.avg.pct_of_peak_sustained_active',
    'dram__throughput.avg.pct_of_peak_sustained_elapsed',
    'lts__throughput.avg.pct_of_peak_sustained_elapsed',
    'gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed',
    'l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed',
    'l1tex__data_bank_writes.avg.pct_of_peak_sustained_elapsed',
    'launch__occupancy_limit_registers',
    'launch__occupancy_limit_shared_mem',
    'launch__occupancy_limit_blocks',
    'smsp__warp_issue_stalled_barrier_per_warp_active.pct',
    'smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct',
    'smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct',
    'smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct',
]


class NcuRichHandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.tempdir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def patch_state_lib_paths(self, repo_root: Path) -> None:
        originals = {}
        for name, value in {
            'REPO_ROOT': repo_root,
            'STATE_DIR': repo_root / 'state',
            'RUNS_DIR': repo_root / 'runs',
            'LATEST_RUN_PATH': repo_root / 'state' / 'latest_run.json',
            'LATEST_NCU_SUMMARY_PATH': repo_root / 'state' / 'latest_ncu_summary.json',
        }.items():
            originals[name] = getattr(state_lib, name)
            setattr(state_lib, name, value)
        self.addCleanup(self.restore_state_lib_paths, originals)

    def restore_state_lib_paths(self, originals: dict[str, object]) -> None:
        for name, value in originals.items():
            setattr(state_lib, name, value)

    def stage_run_dir(
        self,
        run_name: str,
        *,
        headline_fixture: str,
        import_raw_fixture: str,
        details_fixture: str | None = None,
        source_fixture: str | None = None,
    ) -> Path:
        run_dir = self.tmp / 'runs' / run_name
        run_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FIXTURE_DIR / headline_fixture, run_dir / 'ncu_metrics.csv')
        shutil.copyfile(FIXTURE_DIR / import_raw_fixture, run_dir / 'ncu_import_raw.csv')
        shutil.copyfile(FIXTURE_DIR / import_raw_fixture, run_dir / 'ncu_details.csv')
        if details_fixture:
            shutil.copyfile(FIXTURE_DIR / details_fixture, run_dir / 'ncu_details_page.csv')
        if source_fixture:
            shutil.copyfile(FIXTURE_DIR / source_fixture, run_dir / 'ncu_source.csv')
        (run_dir / 'ncu_profile.ncu-rep').write_text('fixture report\n', encoding='utf-8')
        return run_dir

    def write_run_summary(self, run_dir: Path, *, runtime_ms: float, tflops: float) -> None:
        payload = {
            'kernel_tag': 'fixture_kernel',
            'runner': 'build/custom_runner',
            'dataset_id': 'fixed_bf16_gemm_v1',
            'benchmark_case': 'case_00_seed_3407',
            'correctness_runs': [
                {'case_id': 'case_00_seed_3407', 'passed': True},
            ],
            'perf_run': {
                'passed': True,
                'runtime_ms': {
                    'median': runtime_ms,
                    'p10': runtime_ms - 0.2,
                    'p90': runtime_ms + 0.2,
                },
                'tflops': tflops,
            },
        }
        (run_dir / 'summary.json').write_text(json.dumps(payload), encoding='utf-8')

    def analyze_fixture_run(
        self,
        run_dir: Path,
        *,
        details_available: bool,
        source_available: bool,
        previous_analysis_path: Path | None = None,
        source_unavailable_reason: str | None = None,
    ) -> tuple[dict, Path, Path]:
        details_page = run_dir / 'ncu_details_page.csv'
        source_page = run_dir / 'ncu_source.csv'
        analysis = ncu_analysis.analyze_run(
            run_dir=run_dir,
            source_run_id=run_dir.name,
            headline_csv_path=run_dir / 'ncu_metrics.csv',
            import_raw_path=run_dir / 'ncu_import_raw.csv',
            details_page_path=details_page if details_available else None,
            source_csv_path=source_page if source_available else None,
            rep_path=run_dir / 'ncu_profile.ncu-rep',
            wanted_headline_metrics=HEADLINE_METRICS,
            previous_analysis_path=previous_analysis_path,
            source_unavailable_reason=source_unavailable_reason,
            details_unavailable_reason=None if details_available else 'details page not exported in fixture',
            import_raw_unavailable_reason=None,
            legacy_import_raw_alias=run_dir / 'ncu_details.csv',
            return_codes={
                'rep': 0,
                'headline_csv': 0,
                'import_raw': 0,
                'details_page': 0 if details_available else None,
                'source_page': 0 if source_available else 1,
            },
        )
        analysis_json_path, analysis_md_path = ncu_analysis.write_analysis_outputs(run_dir=run_dir, analysis=analysis)
        return analysis, analysis_json_path, analysis_md_path

    def test_parsers_cover_headline_import_details_and_source_pages(self) -> None:
        headline_records = ncu_analysis.parse_wide_csv_records(FIXTURE_DIR / 'headline_metrics.csv')
        import_raw_records = ncu_analysis.parse_wide_csv_records(FIXTURE_DIR / 'import_raw.csv')
        details_rows = ncu_analysis.parse_generic_rows(FIXTURE_DIR / 'details_page.csv')
        source_rows = ncu_analysis.parse_generic_rows(FIXTURE_DIR / 'source_page.csv')

        self.assertEqual(len(headline_records), 1)
        self.assertEqual(len(import_raw_records), 1)
        launch = ncu_analysis.build_launch(headline_records[0], import_raw_records[0])
        self.assertEqual(launch['kernel_name'], 'bf16_gemm_kernel')
        self.assertEqual(launch['block_size'], '128x128x1')
        self.assertEqual(launch['registers_per_thread'], 96.0)
        self.assertEqual(launch['shared_mem_per_block_allocated'], 49152.0)

        rules = ncu_analysis.build_rules(details_rows, 'bf16_gemm_kernel')
        self.assertGreaterEqual(len(rules), 2)
        self.assertEqual(rules[0]['rule_name'], 'Uncoalesced global accesses')

        hotspot = ncu_analysis.build_hotspot_from_row(source_rows[0], index=0)
        self.assertIsNotNone(hotspot)
        self.assertEqual(hotspot['scope_type'], 'cuda_source')
        self.assertEqual(hotspot['scope_name'], 'gemm_mainloop')
        self.assertEqual(hotspot['location'], 'src/kernels/bf16_gemm_v1.cu:412')

    def test_analysis_computes_structured_deltas_and_hotspots(self) -> None:
        previous_run_dir = self.stage_run_dir(
            '20260421_prev_fixture',
            headline_fixture='headline_metrics_prev.csv',
            import_raw_fixture='import_raw_prev.csv',
            source_fixture='source_page_prev.csv',
        )
        previous_analysis, previous_json_path, _ = self.analyze_fixture_run(
            previous_run_dir,
            details_available=False,
            source_available=True,
        )

        current_run_dir = self.stage_run_dir(
            '20260421_curr_fixture',
            headline_fixture='headline_metrics.csv',
            import_raw_fixture='import_raw.csv',
            details_fixture='details_page.csv',
            source_fixture='source_page.csv',
        )
        current_analysis, _, _ = self.analyze_fixture_run(
            current_run_dir,
            details_available=True,
            source_available=True,
            previous_analysis_path=previous_json_path,
        )

        hotspot = current_analysis['source_hotspots'][0]
        for key in (
            'hotspot_id',
            'scope_type',
            'scope_name',
            'location',
            'metric_name',
            'metric_value',
            'importance_score',
            'explanation',
        ):
            self.assertIn(key, hotspot)

        delta_summary = current_analysis['delta_vs_previous_run']
        self.assertEqual(delta_summary['baseline_run_id'], previous_analysis['source_run_id'])
        self.assertGreaterEqual(len(delta_summary['stall_breakdown']), 1)
        self.assertGreaterEqual(len(delta_summary['source_hotspots']['improved']), 1)
        self.assertGreaterEqual(len(delta_summary['source_hotspots']['regressed']), 1)
        self.assertGreaterEqual(len(delta_summary['source_hotspots']['new']), 1)

        class_ids = [item['class_id'] for item in current_analysis['bottleneck_classes']]
        self.assertIn('global_memory_bound', class_ids)
        self.assertTrue(current_analysis['handoff']['node_b']['top_findings'])
        self.assertTrue(current_analysis['handoff']['node_c']['target_hotspots'])

    def test_summary_schema_and_contexts_include_rich_handoff(self) -> None:
        previous_run_dir = self.stage_run_dir(
            '20260421_prev_context',
            headline_fixture='headline_metrics_prev.csv',
            import_raw_fixture='import_raw_prev.csv',
            source_fixture='source_page_prev.csv',
        )
        _, previous_json_path, _ = self.analyze_fixture_run(
            previous_run_dir,
            details_available=False,
            source_available=True,
        )

        current_run_dir = self.stage_run_dir(
            '20260421_curr_context',
            headline_fixture='headline_metrics.csv',
            import_raw_fixture='import_raw.csv',
            details_fixture='details_page.csv',
            source_fixture='source_page.csv',
        )
        _, _, _ = self.analyze_fixture_run(
            current_run_dir,
            details_available=True,
            source_available=True,
            previous_analysis_path=previous_json_path,
        )
        self.write_run_summary(current_run_dir, runtime_ms=12.4, tflops=59.8)

        latest_run, latest_ncu, _ = graph.summarize_run(
            current_run_dir,
            measured_commit='abc1234',
            benchmark_state=default_benchmark_state(),
        )

        state_dir = self.tmp / 'state'
        state_dir.mkdir(parents=True, exist_ok=True)
        summary_json_path = state_dir / 'latest_ncu_summary.json'
        summary_md_path = state_dir / 'latest_ncu_summary.md'
        summary_json_path.write_text(json.dumps(latest_ncu, indent=2), encoding='utf-8')
        summary_md_path.write_text(graph.render_latest_ncu_md(latest_ncu), encoding='utf-8')

        stored_summary = json.loads(summary_json_path.read_text(encoding='utf-8'))
        self.assertEqual(stored_summary['schema_version'], 2)
        self.assertEqual(stored_summary['launch']['kernel_name'], 'bf16_gemm_kernel')
        self.assertTrue(stored_summary['top_findings'])
        self.assertTrue(stored_summary['top_source_hotspots'])
        self.assertEqual(
            stored_summary['delta_vs_previous_run']['baseline_run_id'],
            '20260421_prev_context',
        )

        rendered_summary = summary_md_path.read_text(encoding='utf-8')
        self.assertIn('## Launch / kernel metadata', rendered_summary)
        self.assertIn('## Primary bottlenecks', rendered_summary)
        self.assertIn('## Top hotspots', rendered_summary)
        self.assertIn('## Delta vs previous run', rendered_summary)
        self.assertIn('## Handoff to node_b', rendered_summary)
        self.assertIn('## Handoff to node_c', rendered_summary)

        diagnosis_direction = {
            'direction_id': 'dir_01',
            'name': 'Retune mainloop global loads',
            'family_id': 'family::memory',
            'subfamily_id': 'family::memory::global_loads',
            'action_fingerprint': 'fp::retune_mainloop_global_loads',
            'mode': 'exploit',
            'hypothesis': 'The dominant global-memory hotspot should improve if the mainloop load cadence is tightened.',
            'expected_bottleneck': 'global_memory_bound',
            'code_locations': ['src/kernels/bf16_gemm_v1.cu:412'],
            'risk': 'medium',
            'metrics_to_recheck': ['dram__throughput.avg.pct_of_peak_sustained_elapsed'],
            'search_score_v1': 1.5,
            'score_breakdown': {'policy_id': 'fixture'},
            'predicted_gain_ms': 0.2,
            'predicted_fail_risk': 0.35,
            'ranking_notes': ['Use the mainloop hotspot as the primary recheck anchor.'],
            'stop_condition': 'Stop if tensor activity drops or new barrier hotspots appear.',
            'evidence_refs': ['state/latest_ncu_summary.md', latest_run['ncu_analysis_path']],
            'target_hotspots': latest_ncu['handoff']['node_c']['target_hotspots'][:2],
            'expected_local_changes': ['Reduce replay-heavy mainloop global-load pressure around the dominant source hotspot.'],
            'guardrail_metrics': latest_ncu['handoff']['node_c']['guardrail_metrics'][:2],
        }
        diagnosis = {
            'status': 'awaiting_codex',
            'recommended_direction_id': 'dir_01',
            'directions': [diagnosis_direction],
        }
        active_direction = {
            'direction_id': 'dir_01',
            'candidate_id': 'diag_fixture:dir_01',
            'base_run_id': latest_run['run_id'],
            'family_id': diagnosis_direction['family_id'],
            'action_fingerprint': diagnosis_direction['action_fingerprint'],
            'selection_mode': 'recommended_direction',
            'source_diagnosis_id': 'diag_fixture',
            'summary': diagnosis_direction,
        }
        graph_state = {'current_kernel_path': 'src/kernels/bf16_gemm_v1.cu'}

        node_b_context = graph.render_node_b_context(
            graph_state,
            latest_run,
            latest_ncu,
            diagnosis,
            {'active': False, 'remaining_rounds': 0},
        )
        self.assertIn('Prioritize the structured bottleneck / hotspot / delta handoff first.', node_b_context)
        self.assertIn('ncu_analysis.md', node_b_context)
        self.assertIn('ncu_details_page.csv', node_b_context)

        node_c_context = graph.render_node_c_context(
            graph_state,
            latest_run,
            latest_ncu,
            diagnosis,
            active_direction,
            [],
            {'active': False, 'remaining_rounds': 0},
        )
        self.assertIn('## Relevant hotspots', node_c_context)
        self.assertIn('## Guardrail metrics', node_c_context)
        self.assertIn('## Delta vs previous run', node_c_context)
        self.assertIn('## Finalize recheck points', node_c_context)
        self.assertIn('gemm_mainloop', node_c_context)

    def test_source_page_unavailable_falls_back_without_failing(self) -> None:
        run_dir = self.stage_run_dir(
            '20260421_source_unavailable',
            headline_fixture='headline_metrics.csv',
            import_raw_fixture='import_raw.csv',
            details_fixture='details_page.csv',
        )
        analysis, _, _ = self.analyze_fixture_run(
            run_dir,
            details_available=True,
            source_available=False,
            source_unavailable_reason='source correlation missing in fixture',
        )

        self.assertEqual(analysis['status'], 'available')
        self.assertEqual(analysis['artifacts']['source_page']['status'], 'unavailable')
        self.assertIn('source correlation missing in fixture', analysis['artifacts']['source_page']['unavailable_reason'])
        self.assertTrue(analysis['source_hotspots'])
        self.assertTrue(analysis['handoff']['node_b']['top_findings'])

    def test_load_latest_ncu_summary_hydrates_from_latest_run_when_state_is_shallow(self) -> None:
        repo_root = self.tmp
        state_dir = repo_root / 'state'
        state_dir.mkdir(parents=True, exist_ok=True)

        run_dir = self.stage_run_dir(
            '20260421_hydrate_current',
            headline_fixture='headline_metrics.csv',
            import_raw_fixture='import_raw.csv',
            details_fixture='details_page.csv',
            source_fixture='source_page.csv',
        )
        analysis, analysis_json_path, _ = self.analyze_fixture_run(
            run_dir,
            details_available=True,
            source_available=True,
        )
        run_summary = ncu_analysis.build_rich_summary_from_analysis(analysis)
        run_summary['analysis_path'] = analysis_json_path.name
        (run_dir / 'ncu_summary.json').write_text(json.dumps(run_summary, indent=2), encoding='utf-8')

        latest_run_payload = {
            'run_id': run_dir.name,
            'run_dir': f'runs/{run_dir.name}',
        }
        shallow_state_summary = {
            'status': 'available',
            'source_run_id': 'older_run',
            'headline_metrics': {
                'sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active': 11.0,
            },
        }
        (state_dir / 'latest_run.json').write_text(json.dumps(latest_run_payload, indent=2), encoding='utf-8')
        (state_dir / 'latest_ncu_summary.json').write_text(json.dumps(shallow_state_summary, indent=2), encoding='utf-8')

        self.patch_state_lib_paths(repo_root)
        hydrated = state_lib.load_latest_ncu_summary()

        self.assertEqual(hydrated['schema_version'], 2)
        self.assertEqual(hydrated['source_run_id'], run_dir.name)
        self.assertEqual(hydrated['analysis_path'], f'runs/{run_dir.name}/ncu_analysis.json')
        self.assertTrue(hydrated['top_findings'])
        self.assertTrue(hydrated['handoff']['node_b']['top_findings'])


if __name__ == '__main__':
    unittest.main()
