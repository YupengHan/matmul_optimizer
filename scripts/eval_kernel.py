#!/usr/bin/env python3
"""
Evaluation orchestrator for kernel candidates.

This script is intentionally "script-first":
- it does not reason about optimization strategy,
- it executes the benchmark contract,
- it writes machine-readable and human-readable run artifacts.

Expected external runner contract
---------------------------------
You provide a benchmark runner binary or script via --runner.

The runner is expected to support at least:

    --dataset-dir <path>
    --case-id <case_id>
    --mode <correctness|perf>
    --warmup <int>
    --iters <int>
    --flush-cache-mb <int>
    --json-out <path>

The runner should emit a JSON file with fields such as:
    {
      "mode": "perf",
      "passed": true,
      "runtime_ms": {
        "median": 12.34,
        "p10": 12.10,
        "p90": 12.60
      },
      "tflops": 58.9,
      "correctness": {
        "max_abs_err": ...,
        "max_rel_err": ...,
        "mean_abs_err": ...
      }
    }

This script can still be useful before the runner exists because it fixes
the artifact layout and the run protocol.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

import ncu_analysis


def load_json(path: Path) -> Dict:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path: Path, payload: Dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + '\n', encoding='utf-8')


def read_metrics_file(path: Optional[Path]) -> List[str]:
    if path is None or not path.exists():
        return []
    lines = []
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if line and not line.startswith('#'):
            lines.append(line)
    return lines


def render_markdown_summary(summary: Dict) -> str:
    lines: List[str] = []
    lines.append('# Run summary')
    lines.append('')
    lines.append(f"- kernel tag: `{summary['kernel_tag']}`")
    lines.append(f"- timestamp: `{summary['timestamp']}`")
    lines.append(f"- dataset: `{summary['dataset_id']}`")
    lines.append(f"- benchmark case: `{summary['benchmark_case']}`")
    lines.append(f"- runner: `{summary['runner']}`")
    lines.append('')

    lines.append('## Correctness')
    if not summary['correctness_runs']:
        lines.append('')
        lines.append('No correctness runs were executed.')
    else:
        lines.append('')
        for item in summary['correctness_runs']:
            status = 'PASS' if item.get('passed') else 'FAIL'
            lines.append(f"### {item['case_id']}")
            lines.append(f"- status: **{status}**")
            if 'correctness' in item:
                corr = item['correctness']
                lines.append(f"- max abs err: `{corr.get('max_abs_err', 'N/A')}`")
                lines.append(f"- max rel err: `{corr.get('max_rel_err', 'N/A')}`")
                lines.append(f"- mean abs err: `{corr.get('mean_abs_err', 'N/A')}`")
            lines.append('')

    lines.append('## Performance')
    perf = summary.get('perf_run')
    lines.append('')
    if perf is None:
        lines.append('No performance run was executed.')
    else:
        status = 'PASS' if perf.get('passed') else 'FAIL'
        lines.append(f"- status: **{status}**")
        runtime = perf.get('runtime_ms', {})
        lines.append(f"- median runtime (ms): `{runtime.get('median', 'N/A')}`")
        lines.append(f"- p10 runtime (ms): `{runtime.get('p10', 'N/A')}`")
        lines.append(f"- p90 runtime (ms): `{runtime.get('p90', 'N/A')}`")
        lines.append(f"- TFLOP/s: `{perf.get('tflops', 'N/A')}`")

    lines.append('')
    lines.append('## Nsight Compute')
    lines.append('')
    if summary.get('ncu') is None:
        lines.append('Nsight Compute was not run.')
    else:
        ncu = summary['ncu']
        lines.append(f"- rep path: `{ncu.get('rep_path', 'N/A')}`")
        lines.append(f"- csv path: `{ncu.get('csv_path', 'N/A')}`")
        lines.append(f"- imported raw csv path: `{ncu.get('import_raw_csv_path', 'N/A')}`")
        lines.append(f"- details page csv path: `{ncu.get('details_page_csv_path', 'N/A')}`")
        lines.append(f"- source page csv path: `{ncu.get('source_csv_path', 'N/A')}`")
        lines.append(f"- ncu summary json: `{ncu.get('summary_json_path', 'N/A')}`")
        lines.append(f"- ncu summary md: `{ncu.get('summary_md_path', 'N/A')}`")
        lines.append(f"- ncu analysis json: `{ncu.get('analysis_json_path', 'N/A')}`")
        lines.append(f"- ncu analysis md: `{ncu.get('analysis_md_path', 'N/A')}`")
        if ncu.get('headline_metrics'):
            lines.append('')
            lines.append('### Headline metrics')
            for k, v in ncu['headline_metrics'].items():
                lines.append(f"- `{k}`: `{v}`")

    return '\n'.join(lines) + '\n'


def build_ncu_summary(
    *,
    full_metrics: Dict[str, object],
    headline_metrics: Dict[str, object],
    csv_path: Path,
    rep_path: Path,
    import_raw_path: Optional[Path],
    details_page_path: Optional[Path],
    source_csv_path: Optional[Path],
    legacy_import_raw_alias: Optional[Path],
    analysis: Optional[Dict[str, object]],
    analysis_json_path: Optional[Path],
) -> Dict:
    if analysis:
        summary = ncu_analysis.build_rich_summary_from_analysis(analysis)
        summary['analysis_path'] = analysis_json_path.name if analysis_json_path else None
        return summary

    launch = {
        'kernel_name': full_metrics.get('Kernel Name'),
        'block_size': full_metrics.get('Block Size') or full_metrics.get('launch__block_size'),
        'grid_size': full_metrics.get('Grid Size') or full_metrics.get('launch__grid_size'),
        'registers_per_thread': full_metrics.get('launch__registers_per_thread'),
        'shared_mem_per_block_allocated': full_metrics.get('launch__shared_mem_per_block_allocated'),
    }
    return {
        'schema_version': 2,
        'status': 'available' if headline_metrics or full_metrics else 'available_without_parsed_metrics',
        'source_run_id': None,
        'source_run_dir': None,
        'analysis_path': analysis_json_path.name if analysis_json_path else None,
        'kernel_name': launch.get('kernel_name'),
        'block_size': launch.get('block_size'),
        'grid_size': launch.get('grid_size'),
        'registers_per_thread': launch.get('registers_per_thread'),
        'shared_mem_per_block_allocated': launch.get('shared_mem_per_block_allocated'),
        'launch': launch,
        'headline_metrics': headline_metrics,
        'stall_breakdown': [],
        'bottleneck_classes': [],
        'top_findings': [],
        'top_source_hotspots': [],
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
        'raw_csv_path': csv_path.name if csv_path.exists() else None,
        'raw_rep_path': rep_path.name if rep_path.exists() else None,
        'raw_details_csv_path': legacy_import_raw_alias.name if legacy_import_raw_alias and legacy_import_raw_alias.exists() else None,
        'import_raw_csv_path': import_raw_path.name if import_raw_path and import_raw_path.exists() else None,
        'details_page_csv_path': details_page_path.name if details_page_path and details_page_path.exists() else None,
        'source_csv_path': source_csv_path.name if source_csv_path and source_csv_path.exists() else None,
        'artifacts': {},
    }


def render_markdown_ncu_summary(summary: Dict) -> str:
    lines: List[str] = []
    lines.append('# Nsight Compute summary')
    lines.append('')
    lines.append(f"- schema version: `{summary.get('schema_version', 'N/A')}`")
    lines.append(f"- status: `{summary.get('status', 'unknown')}`")
    lines.append(f"- raw csv path: `{summary.get('raw_csv_path', 'N/A')}`")
    lines.append(f"- raw rep path: `{summary.get('raw_rep_path', 'N/A')}`")
    lines.append(f"- raw detailed csv path: `{summary.get('raw_details_csv_path', 'N/A')}`")
    lines.append(f"- imported raw csv path: `{summary.get('import_raw_csv_path', 'N/A')}`")
    lines.append(f"- details page csv path: `{summary.get('details_page_csv_path', 'N/A')}`")
    lines.append(f"- source csv path: `{summary.get('source_csv_path', 'N/A')}`")
    lines.append(f"- analysis path: `{summary.get('analysis_path', 'N/A')}`")
    lines.append(f"- kernel name: `{summary.get('kernel_name', 'N/A')}`")
    lines.append(f"- block size: `{summary.get('block_size', 'N/A')}`")
    lines.append(f"- grid size: `{summary.get('grid_size', 'N/A')}`")
    lines.append(f"- registers / thread: `{summary.get('registers_per_thread', 'N/A')}`")
    lines.append(f"- shared mem / block allocated: `{summary.get('shared_mem_per_block_allocated', 'N/A')}`")
    lines.append('')
    lines.append('## Headline metrics')
    lines.append('')

    headline_metrics = summary.get('headline_metrics', {})
    if not headline_metrics:
        lines.append('No headline metrics were parsed from the Nsight Compute CSV.')
    else:
        for key, value in headline_metrics.items():
            lines.append(f"- `{key}`: `{value}`")

    top_findings = summary.get('top_findings') or []
    if top_findings:
        lines.append('')
        lines.append('## Top findings')
        lines.append('')
        for item in top_findings[:4]:
            lines.append(f"- `{item.get('finding_type', 'finding')}`: {item.get('summary', 'N/A')}")

    return '\n'.join(lines) + '\n'


def parse_ncu_csv(csv_path: Path) -> Dict[str, str]:
    """
    Best-effort parser for a typical NCU CSV export.

    If parsing fails, return an empty dict. This is fine for an initial scaffold.
    """
    metrics = ncu_analysis.parse_name_value_metrics(csv_path)
    if metrics:
        return {key: value for key, value in metrics.items() if value is not None}
    record = ncu_analysis.select_primary_record(ncu_analysis.parse_wide_csv_records(csv_path))
    if not record:
        return {}
    return {key: value for key, value in record.items() if value not in (None, '')}


def pick_headline_metrics(metrics: Dict[str, str], wanted: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for key in wanted:
        if key in metrics:
            out[key] = metrics[key]
    return out


def summarize_command_failure(stderr_path: Path, fallback: str) -> str:
    if stderr_path.exists():
        lines = [line.strip() for line in stderr_path.read_text(encoding='utf-8', errors='replace').splitlines() if line.strip()]
        if lines:
            return lines[-1]
    return fallback


def cleanup_failed_artifact(path: Path) -> None:
    if path.exists():
        path.unlink()


def run_command(cmd: List[str], cwd: Optional[Path] = None, stdout_path: Optional[Path] = None, stderr_path: Optional[Path] = None) -> int:
    stdout_handle = stdout_path.open('w', encoding='utf-8') if stdout_path else subprocess.DEVNULL
    stderr_handle = stderr_path.open('w', encoding='utf-8') if stderr_path else subprocess.DEVNULL
    try:
        proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, stdout=stdout_handle, stderr=stderr_handle, check=False)
        return proc.returncode
    finally:
        if stdout_path:
            stdout_handle.close()
        if stderr_path:
            stderr_handle.close()


def runner_base_command(args: argparse.Namespace) -> List[str]:
    if args.runner.suffix == '.py':
        return [sys.executable, str(args.runner)]
    return [str(args.runner)]


def run_runner(
    args: argparse.Namespace,
    run_dir: Path,
    dataset_dir: Path,
    case_id: str,
    mode: str,
    warmup: int,
    iters: int,
) -> Dict:
    json_out = run_dir / f"{mode}_{case_id}.json"
    cmd = (
        runner_base_command(args)
        + [
            '--dataset-dir', str(dataset_dir),
            '--case-id', case_id,
            '--mode', mode,
            '--warmup', str(warmup),
            '--iters', str(iters),
            '--flush-cache-mb', str(args.flush_cache_mb),
            '--json-out', str(json_out),
        ]
        + list(args.extra_runner_arg)
    )

    stdout_path = run_dir / f"{mode}_{case_id}.stdout.log"
    stderr_path = run_dir / f"{mode}_{case_id}.stderr.log"

    rc = run_command(cmd, cwd=args.workdir, stdout_path=stdout_path, stderr_path=stderr_path)
    if rc != 0:
        return {
            'case_id': case_id,
            'mode': mode,
            'passed': False,
            'error': f'runner exited with code {rc}',
            'stdout_log': stdout_path.name,
            'stderr_log': stderr_path.name,
        }

    if not json_out.exists():
        return {
            'case_id': case_id,
            'mode': mode,
            'passed': False,
            'error': 'runner did not produce expected JSON output',
            'stdout_log': stdout_path.name,
            'stderr_log': stderr_path.name,
        }

    payload = load_json(json_out)
    payload['case_id'] = case_id
    payload['stdout_log'] = stdout_path.name
    payload['stderr_log'] = stderr_path.name
    return payload


def run_ncu(args: argparse.Namespace, run_dir: Path, dataset_dir: Path, case_id: str, headline_metrics: List[str]) -> Optional[Dict]:
    if args.skip_ncu:
        return None

    if shutil.which(args.ncu_bin) is None:
        return {
            'error': f'ncu binary not found: {args.ncu_bin}',
        }

    rep_prefix = run_dir / 'ncu_profile'
    rep_path = Path(f"{rep_prefix}.ncu-rep")
    csv_path = run_dir / 'ncu_metrics.csv'
    import_raw_csv_path = run_dir / 'ncu_import_raw.csv'
    legacy_import_raw_alias = run_dir / 'ncu_details.csv'
    details_page_csv_path = run_dir / 'ncu_details_page.csv'
    source_csv_path = run_dir / 'ncu_source.csv'

    runner_cmd = (
        runner_base_command(args)
        + [
            '--dataset-dir', str(dataset_dir),
            '--case-id', case_id,
            '--mode', 'perf',
            '--warmup', '0',
            '--iters', '1',
            '--flush-cache-mb', str(args.flush_cache_mb),
        ]
        + list(args.extra_runner_arg)
    )

    rep_cmd = [args.ncu_bin, '--force-overwrite', '-o', str(rep_prefix)] + runner_cmd
    rep_rc = run_command(
        rep_cmd,
        cwd=args.workdir,
        stdout_path=run_dir / 'ncu_rep.stdout.log',
        stderr_path=run_dir / 'ncu_rep.stderr.log',
    )

    metrics = read_metrics_file(args.ncu_metrics_file)
    csv_metrics: Dict[str, str] = {}
    csv_rc = None

    if metrics:
        csv_cmd = [
            args.ncu_bin,
            '--csv',
            '--page', 'raw',
            '--metrics', ','.join(metrics),
        ] + runner_cmd
        csv_rc = run_command(
            csv_cmd,
            cwd=args.workdir,
            stdout_path=csv_path,
            stderr_path=run_dir / 'ncu_csv.stderr.log',
        )
        if csv_rc == 0 and csv_path.exists():
            csv_metrics = parse_ncu_csv(csv_path)

    import_raw_rc = None
    details_page_rc = None
    source_rc = None
    import_raw_unavailable_reason = None
    details_unavailable_reason = None
    source_unavailable_reason = None
    if rep_path.exists():
        import_raw_cmd = [
            args.ncu_bin,
            '--import',
            str(rep_path),
            '--csv',
            '--page', 'raw',
        ]
        import_raw_rc = run_command(
            import_raw_cmd,
            cwd=args.workdir,
            stdout_path=import_raw_csv_path,
            stderr_path=run_dir / 'ncu_details.stderr.log',
        )
        if import_raw_rc == 0 and import_raw_csv_path.exists():
            shutil.copyfile(import_raw_csv_path, legacy_import_raw_alias)
        else:
            cleanup_failed_artifact(import_raw_csv_path)
            cleanup_failed_artifact(legacy_import_raw_alias)
            import_raw_unavailable_reason = summarize_command_failure(
                run_dir / 'ncu_details.stderr.log',
                'failed to export imported raw page from the Nsight Compute report',
            )

        details_page_cmd = [
            args.ncu_bin,
            '--import',
            str(rep_path),
            '--csv',
            '--page', 'details',
        ]
        details_page_rc = run_command(
            details_page_cmd,
            cwd=args.workdir,
            stdout_path=details_page_csv_path,
            stderr_path=run_dir / 'ncu_details_page.stderr.log',
        )
        if details_page_rc != 0:
            cleanup_failed_artifact(details_page_csv_path)
            details_unavailable_reason = summarize_command_failure(
                run_dir / 'ncu_details_page.stderr.log',
                'failed to export the details page from the Nsight Compute report',
            )

        source_cmd = [
            args.ncu_bin,
            '--import',
            str(rep_path),
            '--csv',
            '--page', 'source',
        ]
        source_rc = run_command(
            source_cmd,
            cwd=args.workdir,
            stdout_path=source_csv_path,
            stderr_path=run_dir / 'ncu_source.stderr.log',
        )
        if source_rc != 0:
            cleanup_failed_artifact(source_csv_path)
            source_unavailable_reason = summarize_command_failure(
                run_dir / 'ncu_source.stderr.log',
                'source page export is unavailable; source correlation or line info may be missing',
            )

    ncu_summary = None
    analysis_json_path = None
    analysis_md_path = None
    if csv_path.exists() or rep_path.exists():
        full_metrics = parse_ncu_csv(csv_path) if csv_path.exists() else {}
        picked_metrics = pick_headline_metrics(full_metrics, headline_metrics) if full_metrics else {}
        analysis = ncu_analysis.analyze_run(
            run_dir=run_dir,
            source_run_id=run_dir.name,
            headline_csv_path=csv_path if csv_path.exists() else None,
            import_raw_path=import_raw_csv_path if import_raw_csv_path.exists() else None,
            details_page_path=details_page_csv_path if details_page_csv_path.exists() else None,
            source_csv_path=source_csv_path if source_csv_path.exists() else None,
            rep_path=rep_path if rep_path.exists() else None,
            wanted_headline_metrics=headline_metrics,
            previous_analysis_path=args.previous_ncu_analysis,
            source_unavailable_reason=source_unavailable_reason,
            details_unavailable_reason=details_unavailable_reason,
            import_raw_unavailable_reason=import_raw_unavailable_reason,
            legacy_import_raw_alias=legacy_import_raw_alias if legacy_import_raw_alias.exists() else None,
            return_codes={
                'rep': rep_rc,
                'headline_csv': csv_rc,
                'import_raw': import_raw_rc,
                'details_page': details_page_rc,
                'source_page': source_rc,
            },
        )
        analysis_json_path, analysis_md_path = ncu_analysis.write_analysis_outputs(run_dir=run_dir, analysis=analysis)
        ncu_summary = build_ncu_summary(
            full_metrics=full_metrics,
            headline_metrics=picked_metrics,
            csv_path=csv_path,
            rep_path=rep_path,
            import_raw_path=import_raw_csv_path if import_raw_csv_path.exists() else None,
            details_page_path=details_page_csv_path if details_page_csv_path.exists() else None,
            source_csv_path=source_csv_path if source_csv_path.exists() else None,
            legacy_import_raw_alias=legacy_import_raw_alias if legacy_import_raw_alias.exists() else None,
            analysis=analysis,
            analysis_json_path=analysis_json_path,
        )
        ncu_summary_json_path = run_dir / 'ncu_summary.json'
        ncu_summary_md_path = run_dir / 'ncu_summary.md'
        write_json(ncu_summary_json_path, ncu_summary)
        ncu_summary_md_path.write_text(render_markdown_ncu_summary(ncu_summary), encoding='utf-8')
    else:
        ncu_summary_json_path = None
        ncu_summary_md_path = None

    return {
        'rep_return_code': rep_rc,
        'rep_path': rep_path.name if rep_path.exists() else None,
        'csv_return_code': csv_rc,
        'csv_path': csv_path.name if csv_path.exists() else None,
        'details_csv_return_code': import_raw_rc,
        'details_csv_path': legacy_import_raw_alias.name if legacy_import_raw_alias.exists() else None,
        'import_raw_csv_return_code': import_raw_rc,
        'import_raw_csv_path': import_raw_csv_path.name if import_raw_csv_path.exists() else None,
        'details_page_csv_return_code': details_page_rc,
        'details_page_csv_path': details_page_csv_path.name if details_page_csv_path.exists() else None,
        'source_csv_return_code': source_rc,
        'source_csv_path': source_csv_path.name if source_csv_path.exists() else None,
        'headline_metrics': pick_headline_metrics(csv_metrics, headline_metrics) if csv_metrics else {},
        'summary_json_path': ncu_summary_json_path.name if ncu_summary_json_path else None,
        'summary_md_path': ncu_summary_md_path.name if ncu_summary_md_path else None,
        'analysis_json_path': analysis_json_path.name if analysis_json_path else None,
        'analysis_md_path': analysis_md_path.name if analysis_md_path else None,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Evaluate a kernel candidate and write run artifacts')
    parser.add_argument('--runner', type=Path, required=True, help='External benchmark runner binary or Python script')
    parser.add_argument('--kernel-tag', required=True, help='Human-readable kernel tag for artifact naming')
    parser.add_argument('--config', type=Path, default=Path('configs/fixed_bf16_gemm_v1.json'), help='Dataset config JSON')
    parser.add_argument('--dataset-root', type=Path, default=Path('artifacts/datasets'), help='Generated dataset root')
    parser.add_argument('--runs-root', type=Path, default=Path('runs'), help='Run artifact root')
    parser.add_argument('--workdir', type=Path, default=None, help='Optional working directory for the runner')
    parser.add_argument('--warmup', type=int, default=None, help='Override warmup iterations')
    parser.add_argument('--iters', type=int, default=None, help='Override timed iterations')
    parser.add_argument('--flush-cache-mb', type=int, default=256, help='Scratch size to request from runner')
    parser.add_argument('--skip-correctness', action='store_true', help='Skip correctness runs')
    parser.add_argument('--skip-perf', action='store_true', help='Skip performance run')
    parser.add_argument('--skip-ncu', action='store_true', help='Skip Nsight Compute')
    parser.add_argument('--ncu-bin', default='ncu', help='Nsight Compute CLI binary')
    parser.add_argument('--ncu-metrics-file', type=Path, default=Path('configs/ncu_metrics_core.txt'), help='Text file with one metric name per line')
    parser.add_argument('--previous-ncu-analysis', type=Path, default=None, help='Optional previous ncu_analysis.json for delta-vs-previous-run computation')
    parser.add_argument('--extra-runner-arg', action='append', default=[], help='Extra arg appended to the runner command; may be passed multiple times')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_json(args.config)
    dataset_id = config['dataset_id']
    dataset_dir = args.dataset_root / dataset_id
    if not dataset_dir.exists():
        raise FileNotFoundError(
            f"Dataset directory not found: {dataset_dir}. Generate it first with scripts/generate_fixed_bf16_dataset.py"
        )

    if not args.runner.exists():
        raise FileNotFoundError(f"Runner not found: {args.runner}")

    benchmark_policy = config['benchmark_policy']
    benchmark_case = benchmark_policy['benchmark_case']
    correctness_cases = list(benchmark_policy['correctness_cases'])

    warmup = args.warmup if args.warmup is not None else int(benchmark_policy['warmup_iterations'])
    iters = args.iters if args.iters is not None else int(benchmark_policy['timed_iterations'])

    timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    run_dir = args.runs_root / f"{timestamp}_{args.kernel_tag}"
    run_dir.mkdir(parents=True, exist_ok=False)

    summary: Dict = {
        'timestamp': timestamp,
        'kernel_tag': args.kernel_tag,
        'dataset_id': dataset_id,
        'dataset_dir': str(dataset_dir),
        'benchmark_case': benchmark_case,
        'runner': str(args.runner),
        'correctness_runs': [],
        'perf_run': None,
        'ncu': None,
    }

    if not args.skip_correctness:
        for case_id in correctness_cases:
            payload = run_runner(args, run_dir, dataset_dir, case_id, 'correctness', warmup=0, iters=1)
            summary['correctness_runs'].append(payload)

    if not args.skip_perf:
        summary['perf_run'] = run_runner(args, run_dir, dataset_dir, benchmark_case, 'perf', warmup=warmup, iters=iters)

    headline_metrics = read_metrics_file(args.ncu_metrics_file)
    summary['ncu'] = run_ncu(args, run_dir, dataset_dir, benchmark_case, headline_metrics=headline_metrics)

    write_json(run_dir / 'summary.json', summary)
    (run_dir / 'summary.md').write_text(render_markdown_summary(summary), encoding='utf-8')

    print(f"[done] wrote run artifacts to {run_dir}")


if __name__ == '__main__':
    main()
