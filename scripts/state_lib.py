#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = REPO_ROOT / 'state'
RUNS_DIR = REPO_ROOT / 'runs'
DOCS_DIR = REPO_ROOT / 'docs'
SCRIPTS_DIR = REPO_ROOT / 'scripts'
SRC_DIR = REPO_ROOT / 'src'

GRAPH_STATE_PATH = STATE_DIR / 'graph_state.json'
LATEST_RUN_PATH = STATE_DIR / 'latest_run.json'
LATEST_NCU_SUMMARY_PATH = STATE_DIR / 'latest_ncu_summary.json'
LATEST_DIAGNOSIS_PATH = STATE_DIR / 'latest_diagnosis.json'
ACTIVE_DIRECTION_PATH = STATE_DIR / 'active_direction.json'
BENCHMARK_STATE_PATH = STATE_DIR / 'benchmark_state.json'
RUN_REGISTRY_PATH = STATE_DIR / 'run_registry.jsonl'
ROUND_LOOP_STATE_PATH = STATE_DIR / 'round_loop_state.json'
ROUND_HISTORY_PATH = STATE_DIR / 'round_history.jsonl'
DIAGNOSIS_HISTORY_PATH = STATE_DIR / 'diagnosis_history.jsonl'
SUPERVISOR_TASK_PATH = STATE_DIR / 'supervisor_task.json'
SEARCH_STATE_PATH = STATE_DIR / 'search_state.json'
SEARCH_FRONTIER_PATH = STATE_DIR / 'search_frontier.json'
SEARCH_CLOSED_PATH = STATE_DIR / 'search_closed.jsonl'
FAMILY_LEDGER_PATH = STATE_DIR / 'family_ledger.json'
SEARCH_CANDIDATES_PATH = STATE_DIR / 'search_candidates.json'
LATEST_ATTEMPT_PATH = STATE_DIR / 'latest_attempt.json'


def now_local_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec='seconds')


def timestamp_tag() -> str:
    return dt.datetime.now().strftime('%Y%m%d_%H%M%S')


def repo_rel(path: Path | str | None) -> Optional[str]:
    if path is None:
        return None
    path_obj = Path(path)
    if not path_obj.is_absolute():
        return path_obj.as_posix()
    try:
        return path_obj.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path_obj.as_posix()


def load_json(path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
    if not path.exists():
        return dict(default)
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def load_json_if_exists(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[Dict[str, Any]] = []
    with path.open('r', encoding='utf-8') as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + '\n', encoding='utf-8')


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def append_jsonl(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(payload, sort_keys=False) + '\n')


def touch_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)


def current_kernel_path() -> str:
    kernels = sorted((SRC_DIR / 'kernels').glob('*.cu'))
    if not kernels:
        return 'src/kernels/bf16_gemm_v1.cu'
    return repo_rel(kernels[-1]) or 'src/kernels/bf16_gemm_v1.cu'


def default_graph_state() -> Dict[str, Any]:
    return {
        'current_node': 'node_a',
        'previous_node': None,
        'status': 'ready_for_node_a',
        'latest_run_dir': None,
        'latest_summary_json': repo_rel(LATEST_RUN_PATH),
        'latest_ncu_summary_json': repo_rel(LATEST_NCU_SUMMARY_PATH),
        'latest_commit': None,
        'approved_direction_id': None,
        'recommended_direction_id': None,
        'current_kernel_path': current_kernel_path(),
        'plateau_counter': 0,
        'notes': 'Run node_a to capture a measured custom-kernel snapshot.',
    }


def default_latest_run() -> Dict[str, Any]:
    return {
        'run_id': None,
        'run_dir': None,
        'raw_summary_json': None,
        'raw_summary_md': None,
        'kernel_tag': None,
        'runner': 'build/custom_runner',
        'dataset_id': 'fixed_bf16_gemm_v1',
        'benchmark_case': 'case_00_seed_3407',
        'correctness_passed': None,
        'correctness_cases_total': 0,
        'correctness_cases_passed': 0,
        'perf_passed': None,
        'median_runtime_ms': None,
        'p10_runtime_ms': None,
        'p90_runtime_ms': None,
        'tflops': None,
        'ncu_rep_path': None,
        'ncu_csv_path': None,
        'ncu_analysis_path': None,
        'ncu_summary_json': repo_rel(LATEST_NCU_SUMMARY_PATH),
        'is_new_best_custom': False,
        'measured_commit': None,
        'generated_at': now_local_iso(),
    }


def default_latest_ncu_summary() -> Dict[str, Any]:
    return {
        'schema_version': 2,
        'status': 'missing',
        'source_run_id': None,
        'source_run_dir': None,
        'analysis_path': None,
        'kernel_name': None,
        'block_size': None,
        'grid_size': None,
        'registers_per_thread': None,
        'shared_mem_per_block_allocated': None,
        'launch': {
            'kernel_name': None,
            'block_size': None,
            'grid_size': None,
            'registers_per_thread': None,
            'shared_mem_per_block_allocated': None,
        },
        'headline_metrics': {},
        'stall_breakdown': [],
        'bottleneck_classes': [],
        'top_findings': [],
        'top_source_hotspots': [],
        'handoff': {
            'node_b': {
                'top_findings': [],
                'code_regions_to_investigate': [],
            },
            'node_c': {
                'target_hotspots': [],
                'guardrail_metrics': [],
                'expected_recheck_points': [],
            },
        },
        'delta_vs_previous_run': {
            'baseline_run_id': None,
            'headline_metrics': {},
            'stall_breakdown': [],
            'source_hotspots': {
                'improved': [],
                'regressed': [],
                'new': [],
                'disappeared': [],
            },
        },
        'raw_csv_path': None,
        'raw_rep_path': None,
        'raw_details_csv_path': None,
        'import_raw_csv_path': None,
        'details_page_csv_path': None,
        'source_csv_path': None,
        'artifacts': {},
        'generated_at': now_local_iso(),
    }


def _merge_defaults(payload: Any, defaults: Any) -> Any:
    if isinstance(payload, dict) and isinstance(defaults, dict):
        merged: Dict[str, Any] = {}
        for key, default_value in defaults.items():
            merged[key] = _merge_defaults(payload.get(key), default_value)
        for key, value in payload.items():
            if key not in merged:
                merged[key] = value
        return merged
    if payload is None:
        if isinstance(defaults, dict):
            return {key: _merge_defaults(None, value) for key, value in defaults.items()}
        if isinstance(defaults, list):
            return list(defaults)
        return defaults
    return payload


def _resolve_repo_path(path_str: Optional[str]) -> Optional[Path]:
    if not path_str:
        return None
    path = Path(path_str)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def _repo_rel_run_artifact(run_dir: Path, raw_path: Optional[str]) -> Optional[str]:
    if not raw_path:
        return None
    path = Path(raw_path)
    if path.is_absolute():
        return repo_rel(path)
    if path.parts and path.parts[0] == 'runs':
        return repo_rel(REPO_ROOT / path)
    if path.parts and path.parts[0] == run_dir.name:
        return repo_rel(run_dir.parent / path)
    return repo_rel(run_dir / path)


def _relativize_ncu_summary_paths(run_dir: Path, payload: Dict[str, Any]) -> Dict[str, Any]:
    summary = _merge_defaults(payload, {})
    for key in (
        'analysis_path',
        'raw_csv_path',
        'raw_rep_path',
        'raw_details_csv_path',
        'import_raw_csv_path',
        'details_page_csv_path',
        'source_csv_path',
    ):
        if key in summary:
            summary[key] = _repo_rel_run_artifact(run_dir, summary.get(key))

    artifacts = summary.get('artifacts')
    if isinstance(artifacts, dict):
        for artifact in artifacts.values():
            if not isinstance(artifact, dict):
                continue
            if 'path' in artifact:
                artifact['path'] = _repo_rel_run_artifact(run_dir, artifact.get('path'))
            if 'legacy_alias_path' in artifact:
                artifact['legacy_alias_path'] = _repo_rel_run_artifact(run_dir, artifact.get('legacy_alias_path'))
    return summary


def _has_rich_ncu_handoff(summary: Dict[str, Any]) -> bool:
    if not isinstance(summary, dict):
        return False
    launch = summary.get('launch')
    if isinstance(launch, dict) and any(launch.get(key) is not None for key in (
        'kernel_name',
        'block_size',
        'grid_size',
        'registers_per_thread',
        'shared_mem_per_block_allocated',
    )):
        return True
    if summary.get('analysis_path'):
        return True
    for key in ('bottleneck_classes', 'top_findings', 'top_source_hotspots', 'stall_breakdown'):
        value = summary.get(key)
        if isinstance(value, list) and value:
            return True
    handoff = summary.get('handoff')
    if isinstance(handoff, dict):
        for node_key in ('node_b', 'node_c'):
            node_payload = handoff.get(node_key)
            if isinstance(node_payload, dict) and any(node_payload.values()):
                return True
    return False


def _hydrate_latest_ncu_summary(summary: Dict[str, Any]) -> Dict[str, Any]:
    latest_run = load_json_if_exists(LATEST_RUN_PATH) or default_latest_run()
    latest_run_id = latest_run.get('run_id')
    latest_run_dir = _resolve_repo_path(latest_run.get('run_dir'))
    if not latest_run_id or latest_run_dir is None:
        return _merge_defaults(summary, default_latest_ncu_summary())

    run_summary_path = latest_run_dir / 'ncu_summary.json'
    run_summary = load_json_if_exists(run_summary_path)
    if run_summary is None:
        return _merge_defaults(summary, default_latest_ncu_summary())

    summary_run_id = summary.get('source_run_id')
    needs_hydration = (
        summary_run_id != latest_run_id
        or not _has_rich_ncu_handoff(summary)
    )
    if not needs_hydration:
        return _merge_defaults(summary, default_latest_ncu_summary())

    hydrated = _merge_defaults(
        _relativize_ncu_summary_paths(latest_run_dir, run_summary),
        default_latest_ncu_summary(),
    )
    hydrated['source_run_id'] = latest_run_id
    hydrated['source_run_dir'] = repo_rel(latest_run_dir)
    return hydrated


def default_latest_diagnosis() -> Dict[str, Any]:
    return {
        'diagnosis_id': None,
        'status': 'pending_generation',
        'created_at': None,
        'source_run_id': None,
        'source_run_dir': None,
        'source_summary_json': None,
        'source_ncu_summary_json': repo_rel(LATEST_NCU_SUMMARY_PATH),
        'heuristics_path': 'docs/heuristics.md',
        'current_kernel_path': current_kernel_path(),
        'reasoning_source': None,
        'reasoning_mode': None,
        'reasoning_summary': None,
        'evidence_refs': [],
        'recommended_direction_id': None,
        'approved_direction_id': None,
        'selected_direction_id': None,
        'selected_candidate_id': None,
        'family_audit': [],
        'directions': [],
        'notes': 'Run node_b to produce exactly three ranked directions.',
    }


def default_active_direction() -> Dict[str, Any]:
    return {
        'direction_id': None,
        'name': None,
        'candidate_id': None,
        'selected_from_frontier_id': None,
        'family_id': None,
        'subfamily_id': None,
        'action_fingerprint': None,
        'selection_priority': None,
        'base_run_id': None,
        'selection_mode': None,
        'selected_at': None,
        'source_diagnosis_id': None,
        'secondary_family_ids': [],
        'semantic_delta_tags': [],
        'actual_code_regions': [],
        'implemented_action_fingerprint': None,
        'status': 'idle',
        'summary': None,
        'notes': 'No direction selected yet. Use approve, use-recommended-direction, or select-next after node_b.',
    }


def default_benchmark_state() -> Dict[str, Any]:
    return {
        'dataset_id': 'fixed_bf16_gemm_v1',
        'metric_of_record': 'median_runtime_ms',
        'cutlass_baseline': None,
        'cublas_baseline': None,
        'best_custom': None,
        'updated_at': now_local_iso(),
    }


def default_round_loop_state() -> Dict[str, Any]:
    return {
        'active': False,
        'status': 'idle',
        'total_rounds': 0,
        'completed_rounds': 0,
        'remaining_rounds': 0,
        'next_round_index': 1,
        'current_round_index': None,
        'auto_use_recommended': False,
        'auto_select_frontier': False,
        'started_at': None,
        'completed_at': None,
        'last_completed_round': None,
        'accepted_base_run_id': None,
        'accepted_base_measured_commit': None,
        'accepted_base_runtime_ms': None,
        'history_path': repo_rel(ROUND_HISTORY_PATH),
        'notes': 'No multi-round loop is active. Start one with python scripts/graph.py rounds --count N.',
    }


def default_supervisor_task() -> Dict[str, Any]:
    return {
        'supervisor_role': 'main_llm_agent',
        'dispatch_node': 'node_a',
        'dispatch_mode': 'direct_script',
        'graph_status': 'ready_for_node_a',
        'round_label': 'single-run',
        'round_loop_active': False,
        'rounds_remaining': 0,
        'auto_use_recommended': False,
        'auto_select_frontier': False,
        'requires_gpu_access': True,
        'prepare_command': 'python scripts/graph.py node_a',
        'selection_command': None,
        'finalize_command': None,
        'protocol_doc': 'AGENTS.md',
        'context_file': None,
        'active_direction_id': None,
        'recommended_direction_id': None,
        'context_checkpoint_interval_rounds': 5,
        'last_context_checkpoint_round': None,
        'next_context_checkpoint_round': None,
        'display_update_interval_rounds': 5,
        'last_display_update_round': None,
        'next_display_update_round': None,
        'display_update_due': False,
        'display_update_instruction': None,
        'watchdog_timeout_minutes': 10,
        'watchdog_status': 'idle',
        'watchdog_idle_minutes': None,
        'watchdog_latest_progress_at': None,
        'watchdog_latest_progress_path': None,
        'watchdog_continue_instruction': None,
        'notes': 'Run node_a directly from the main LLM agent.',
    }


def default_search_state() -> Dict[str, Any]:
    return {
        'schema_version': 1,
        'status': 'idle',
        'search_mode': 'family_representative_reopen_v1',
        'search_iteration': 0,
        'goal_summary': 'Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.',
        'target_runtime_ms': None,
        'target_competitor': None,
        'bootstrap_baseline_run_id': None,
        'bootstrap_baseline_measured_commit': None,
        'bootstrap_baseline_runtime_ms': None,
        'bootstrap_started_at': None,
        'accepted_base_run_id': None,
        'accepted_base_measured_commit': None,
        'accepted_base_runtime_ms': None,
        'best_known_run_id': None,
        'best_known_measured_commit': None,
        'best_known_runtime_ms': None,
        'exact_base_run_id': None,
        'exact_base_measured_commit': None,
        'exact_base_runtime_ms': None,
        'active_frontier_id': None,
        'active_candidate_set_id': None,
        'active_candidate_id': None,
        'last_selected_candidate_id': None,
        'last_selected_direction_id': None,
        'last_selected_selection_mode': None,
        'last_selected_at': None,
        'latest_attempt_id': None,
        'last_transition_type': None,
        'last_result_run_id': None,
        'last_result_measured_commit': None,
        'last_result_runtime_ms': None,
        'last_result_correctness_passed': None,
        'last_transition_label': None,
        'last_result_registers_per_thread': None,
        'last_result_shared_mem_per_block_allocated': None,
        'last_restore_run_id': None,
        'last_restore_source_commit': None,
        'last_restore_at': None,
        'last_restore_reason': None,
        'selection_policy': {
            'policy_id': 'family_representative_v2',
            'allow_restore_base': True,
            'max_open_candidates': 3,
            'max_reopens_per_candidate': 1,
            'reopen_loss_tolerance_ms': 0.15,
            'reopen_fail_risk_ceiling': 0.6,
            'family_representatives_only': True,
        },
        'frontier_json': repo_rel(SEARCH_FRONTIER_PATH),
        'candidates_json': repo_rel(SEARCH_CANDIDATES_PATH),
        'closed_jsonl': repo_rel(SEARCH_CLOSED_PATH),
        'family_ledger_json': repo_rel(FAMILY_LEDGER_PATH),
        'latest_attempt_json': repo_rel(LATEST_ATTEMPT_PATH),
        'notes': 'Search scaffolding is idle until a measured base is projected into the persistent family-representative frontier.',
    }


def default_search_frontier() -> Dict[str, Any]:
    return {
        'schema_version': 2,
        'frontier_id': 'frontier:global',
        'status': 'empty',
        'source_run_id': None,
        'source_measured_commit': None,
        'source_diagnosis_id': None,
        'candidate_set_id': None,
        'generated_at': None,
        'updated_at': None,
        'selection_policy_id': 'family_representative_v2',
        'selected_candidate_id': None,
        'selection_reason': None,
        'selection_summary': None,
        'family_representative_count': 0,
        'reopened_candidate_ids': [],
        'candidates': [],
        'notes': 'No persistent frontier history yet. Node B finalize will merge directions into the global family-representative frontier.',
    }


def default_family_ledger() -> Dict[str, Any]:
    return {
        'schema_version': 1,
        'updated_at': now_local_iso(),
        'last_result_run_id': None,
        'last_transition_label': None,
        'families': {},
        'notes': 'Family-level attempt memory is empty until search transitions are recorded.',
    }


def default_search_candidates() -> Dict[str, Any]:
    return {
        'schema_version': 1,
        'candidate_set_id': None,
        'source_run_id': None,
        'source_diagnosis_id': None,
        'generated_at': None,
        'recommended_direction_id': None,
        'recommended_candidate_id': None,
        'candidates': [],
        'notes': 'No normalized candidates yet. Phase 1 will mirror exactly three node_b directions here.',
    }


def default_latest_attempt() -> Dict[str, Any]:
    return {
        'schema_version': 1,
        'attempt_id': None,
        'status': 'idle',
        'candidate_id': None,
        'source_diagnosis_id': None,
        'base_run_id': None,
        'family_id': None,
        'subfamily_id': None,
        'direction_id': None,
        'direction_name': None,
        'mode': None,
        'commit': None,
        'commit_short': None,
        'subject': None,
        'selection_mode': None,
        'selected_at': None,
        'selected_from_frontier_id': None,
        'source_run_id': None,
        'selection_score': None,
        'planned_action_fingerprint': None,
        'implemented_action_fingerprint': None,
        'score_breakdown': {},
        'semantic_delta_tags': [],
        'secondary_family_ids': [],
        'actual_code_regions': [],
        'implementation': {
            'commit': None,
            'commit_short': None,
            'subject': None,
            'build_status': None,
            'failure_mode': None,
            'build_log_path': None,
            'touched_files': [],
            'diff_stats': {
                'files_changed': 0,
                'insertions': 0,
                'deletions': 0,
            },
        },
        'build_status': None,
        'failure_mode': None,
        'diff_stats': {
            'files_changed': 0,
            'insertions': 0,
            'deletions': 0,
        },
        'measurement': {
            'run_id': None,
            'measurement_commit': None,
            'runtime_ms': None,
            'runtime_delta_ms': None,
            'tflops': None,
            'correctness': None,
            'ncu_analysis_path': None,
            'headline_metrics': {},
            'headline_metric_deltas_vs_previous_run': {},
            'structured_bottleneck_deltas': [],
            'top_hotspot_deltas': [],
        },
        'transition_label': None,
        'transition_class': None,
        'close_reason': None,
        'notes': 'No active implementation edge is recorded yet.',
    }


def ensure_machine_state() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not GRAPH_STATE_PATH.exists():
        write_json(GRAPH_STATE_PATH, default_graph_state())
    if not LATEST_RUN_PATH.exists():
        write_json(LATEST_RUN_PATH, default_latest_run())
    if not LATEST_NCU_SUMMARY_PATH.exists():
        write_json(LATEST_NCU_SUMMARY_PATH, default_latest_ncu_summary())
    if not LATEST_DIAGNOSIS_PATH.exists():
        write_json(LATEST_DIAGNOSIS_PATH, default_latest_diagnosis())
    if not ACTIVE_DIRECTION_PATH.exists():
        write_json(ACTIVE_DIRECTION_PATH, default_active_direction())
    if not BENCHMARK_STATE_PATH.exists():
        write_json(BENCHMARK_STATE_PATH, default_benchmark_state())
    if not ROUND_LOOP_STATE_PATH.exists():
        write_json(ROUND_LOOP_STATE_PATH, default_round_loop_state())
    if not SUPERVISOR_TASK_PATH.exists():
        write_json(SUPERVISOR_TASK_PATH, default_supervisor_task())
    if not SEARCH_STATE_PATH.exists():
        write_json(SEARCH_STATE_PATH, default_search_state())
    if not SEARCH_FRONTIER_PATH.exists():
        write_json(SEARCH_FRONTIER_PATH, default_search_frontier())
    if not FAMILY_LEDGER_PATH.exists():
        write_json(FAMILY_LEDGER_PATH, default_family_ledger())
    if not SEARCH_CANDIDATES_PATH.exists():
        write_json(SEARCH_CANDIDATES_PATH, default_search_candidates())
    if not LATEST_ATTEMPT_PATH.exists():
        write_json(LATEST_ATTEMPT_PATH, default_latest_attempt())
    if not SEARCH_CLOSED_PATH.exists():
        touch_file(SEARCH_CLOSED_PATH)


def load_graph_state() -> Dict[str, Any]:
    return load_json(GRAPH_STATE_PATH, default_graph_state())


def load_latest_run() -> Dict[str, Any]:
    return load_json(LATEST_RUN_PATH, default_latest_run())


def load_latest_ncu_summary() -> Dict[str, Any]:
    summary = load_json(LATEST_NCU_SUMMARY_PATH, default_latest_ncu_summary())
    hydrated = _hydrate_latest_ncu_summary(summary)
    normalized = _merge_defaults(hydrated, default_latest_ncu_summary())
    if normalized != summary:
        write_json(LATEST_NCU_SUMMARY_PATH, normalized)
    return normalized


def load_latest_diagnosis() -> Dict[str, Any]:
    return load_json(LATEST_DIAGNOSIS_PATH, default_latest_diagnosis())


def load_active_direction() -> Dict[str, Any]:
    return load_json(ACTIVE_DIRECTION_PATH, default_active_direction())


def load_benchmark_state() -> Dict[str, Any]:
    return load_json(BENCHMARK_STATE_PATH, default_benchmark_state())


def load_round_loop_state() -> Dict[str, Any]:
    return load_json(ROUND_LOOP_STATE_PATH, default_round_loop_state())


def load_supervisor_task() -> Dict[str, Any]:
    return load_json(SUPERVISOR_TASK_PATH, default_supervisor_task())


def load_search_state() -> Dict[str, Any]:
    return load_json(SEARCH_STATE_PATH, default_search_state())


def load_search_frontier() -> Dict[str, Any]:
    return load_json(SEARCH_FRONTIER_PATH, default_search_frontier())


def load_search_closed() -> list[Dict[str, Any]]:
    return load_jsonl(SEARCH_CLOSED_PATH)


def load_family_ledger() -> Dict[str, Any]:
    return load_json(FAMILY_LEDGER_PATH, default_family_ledger())


def load_search_candidates() -> Dict[str, Any]:
    return load_json(SEARCH_CANDIDATES_PATH, default_search_candidates())


def load_latest_attempt() -> Dict[str, Any]:
    return load_json(LATEST_ATTEMPT_PATH, default_latest_attempt())


def load_run_registry() -> list[Dict[str, Any]]:
    return load_jsonl(RUN_REGISTRY_PATH)


def direction_lookup(diagnosis: Dict[str, Any], direction_id: str) -> Optional[Dict[str, Any]]:
    for direction in diagnosis.get('directions', []):
        if direction.get('direction_id') == direction_id:
            return direction
    return None


def ordered_direction_ids(diagnosis: Dict[str, Any]) -> Iterable[str]:
    for direction in diagnosis.get('directions', []):
        direction_id = direction.get('direction_id')
        if direction_id:
            yield direction_id
