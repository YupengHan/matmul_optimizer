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
        lines.append(f"- ncu summary json: `{ncu.get('summary_json_path', 'N/A')}`")
        lines.append(f"- ncu summary md: `{ncu.get('summary_md_path', 'N/A')}`")
        if ncu.get('headline_metrics'):
            lines.append('')
            lines.append('### Headline metrics')
            for k, v in ncu['headline_metrics'].items():
                lines.append(f"- `{k}`: `{v}`")

    return '\n'.join(lines) + '\n'


def build_ncu_summary(metrics: Dict[str, str], csv_path: Path, rep_path: Path) -> Dict:
    return {
        'status': 'available' if metrics else 'available_without_parsed_metrics',
        'kernel_name': metrics.get('Kernel Name'),
        'block_size': metrics.get('Block Size') or metrics.get('launch__block_size'),
        'grid_size': metrics.get('Grid Size') or metrics.get('launch__grid_size'),
        'registers_per_thread': metrics.get('launch__registers_per_thread'),
        'shared_mem_per_block_allocated': metrics.get('launch__shared_mem_per_block_allocated'),
        'headline_metrics': metrics,
        'raw_csv_path': csv_path.name if csv_path.exists() else None,
        'raw_rep_path': rep_path.name if rep_path.exists() else None,
        'raw_details_csv_path': None,
    }


def render_markdown_ncu_summary(summary: Dict) -> str:
    lines: List[str] = []
    lines.append('# Nsight Compute summary')
    lines.append('')
    lines.append(f"- status: `{summary.get('status', 'unknown')}`")
    lines.append(f"- raw csv path: `{summary.get('raw_csv_path', 'N/A')}`")
    lines.append(f"- raw rep path: `{summary.get('raw_rep_path', 'N/A')}`")
    lines.append(f"- raw detailed csv path: `{summary.get('raw_details_csv_path', 'N/A')}`")
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

    return '\n'.join(lines) + '\n'


def parse_ncu_csv(csv_path: Path) -> Dict[str, str]:
    """
    Best-effort parser for a typical NCU CSV export.

    If parsing fails, return an empty dict. This is fine for an initial scaffold.
    """
    try:
        with csv_path.open('r', encoding='utf-8', newline='') as f:
            rows = list(csv.reader(f))
    except Exception:
        return {}

    normalized_rows = [[cell.strip() for cell in row] for row in rows]

    header_idx = None
    metric_name_idx = None
    metric_value_idx = None

    for i, row in enumerate(normalized_rows):
        if 'Metric Name' in row and 'Metric Value' in row:
            header_idx = i
            metric_name_idx = row.index('Metric Name')
            metric_value_idx = row.index('Metric Value')
            break

    if header_idx is not None and metric_name_idx is not None and metric_value_idx is not None:
        metrics: Dict[str, str] = {}
        for row in normalized_rows[header_idx + 1:]:
            if not row:
                continue
            if metric_name_idx >= len(row) or metric_value_idx >= len(row):
                continue
            name = row[metric_name_idx]
            value = row[metric_value_idx]
            if not name:
                continue
            metrics[name] = value
        return metrics

    # Nsight Compute `--csv --page raw` also emits a wide table after a pair of
    # `==PROF==` banner lines. In that layout, row N is the header, row N+1 is
    # mostly units, and row N+2 holds the values for a single kernel launch.
    for i, row in enumerate(normalized_rows):
        if 'ID' not in row:
            continue
        if not any('__' in cell or cell.startswith('launch__') for cell in row):
            continue

        data_row = None
        for candidate in normalized_rows[i + 1:]:
            if len(candidate) != len(row):
                continue
            if candidate and candidate[0]:
                data_row = candidate
                break

        if data_row is None:
            return {}

        metrics = {}
        for name, value in zip(row, data_row):
            if not name or not value:
                continue
            metrics[name] = value
        return metrics

    return {}


def pick_headline_metrics(metrics: Dict[str, str], wanted: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for key in wanted:
        if key in metrics:
            out[key] = metrics[key]
    return out


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
    detailed_csv_path = run_dir / 'ncu_details.csv'

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

    details_rc = None
    if rep_path.exists():
        details_cmd = [
            args.ncu_bin,
            '--import',
            str(rep_path),
            '--csv',
            '--page', 'raw',
        ]
        details_rc = run_command(
            details_cmd,
            cwd=args.workdir,
            stdout_path=detailed_csv_path,
            stderr_path=run_dir / 'ncu_details.stderr.log',
        )
        if details_rc != 0 and detailed_csv_path.exists():
            detailed_csv_path.unlink()

    ncu_summary = None
    if csv_path.exists() or rep_path.exists():
        picked_metrics = pick_headline_metrics(csv_metrics, headline_metrics) if csv_metrics else {}
        ncu_summary = build_ncu_summary(picked_metrics, csv_path, rep_path)
        ncu_summary['raw_details_csv_path'] = detailed_csv_path.name if detailed_csv_path.exists() else None
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
        'details_csv_return_code': details_rc,
        'details_csv_path': detailed_csv_path.name if detailed_csv_path.exists() else None,
        'headline_metrics': pick_headline_metrics(csv_metrics, headline_metrics) if csv_metrics else {},
        'summary_json_path': ncu_summary_json_path.name if ncu_summary_json_path else None,
        'summary_md_path': ncu_summary_md_path.name if ncu_summary_md_path else None,
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
