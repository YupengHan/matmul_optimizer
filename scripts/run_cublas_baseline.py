#!/usr/bin/env python3
"""
Thin wrapper around eval_kernel.py for the cuBLAS reference runner.

Usage example:
    cmake -S . -B build -DENABLE_CUBLAS_RUNNER=ON
    cmake --build build -j 4 --target cublas_runner
    python scripts/run_cublas_baseline.py \
        --runner ./build/cublas_runner \
        --kernel-tag cublas_ref_v0

This wrapper also updates state/benchmark_state.json and
state/benchmark_baselines.md after a successful run so cuBLAS becomes a
first-class reference for progress tracking and node_b context.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from gpu_lock import gpu_exclusive
from graph import refresh_all_views, render_benchmark_baselines_md
from state_lib import BENCHMARK_STATE_PATH, REPO_ROOT, load_benchmark_state, now_local_iso, repo_rel, write_json, write_text

DONE_PREFIX = '[done] wrote run artifacts to '


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Run the cuBLAS baseline through eval_kernel.py')
    parser.add_argument('--runner', type=Path, required=True, help='cuBLAS benchmark runner binary or Python script')
    parser.add_argument('--kernel-tag', default='cublas_ref', help='Kernel tag used in the run artifact directory')
    parser.add_argument('--config', type=Path, default=Path('configs/fixed_bf16_gemm_v1.json'))
    parser.add_argument('--dataset-root', type=Path, default=Path('artifacts/datasets'))
    parser.add_argument('--runs-root', type=Path, default=Path('runs'))
    parser.add_argument('--workdir', type=Path, default=None)
    parser.add_argument('--warmup', type=int, default=None)
    parser.add_argument('--iters', type=int, default=None)
    parser.add_argument('--flush-cache-mb', type=int, default=256)
    parser.add_argument('--skip-ncu', action='store_true')
    parser.add_argument('--ncu-bin', default='ncu', help='Nsight Compute CLI binary')
    parser.add_argument('--ncu-metrics-file', type=Path, default=Path('configs/ncu_metrics_core.txt'))
    parser.add_argument('--extra-runner-arg', action='append', default=[], help='Extra arg appended to the cuBLAS runner; may be passed multiple times')
    return parser.parse_args()


def parse_run_dir(stdout: str) -> Path:
    for raw in reversed(stdout.splitlines()):
        line = raw.strip()
        if line.startswith(DONE_PREFIX):
            return Path(line[len(DONE_PREFIX):].strip())
    raise RuntimeError('could not parse run directory from eval_kernel.py output')


def load_json(path: Path) -> dict:
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def update_cublas_baseline(run_dir: Path) -> None:
    summary_path = run_dir / 'summary.json'
    summary = load_json(summary_path)
    correctness_runs = summary.get('correctness_runs') or []
    perf_run = summary.get('perf_run') or {}
    correctness_passed = bool(perf_run.get('passed')) and all(item.get('passed') for item in correctness_runs)

    benchmark_state = load_benchmark_state()
    benchmark_state['cublas_baseline'] = {
        'run_id': run_dir.name,
        'run_dir': repo_rel(run_dir),
        'kernel_tag': summary.get('kernel_tag'),
        'median_runtime_ms': (perf_run.get('runtime_ms') or {}).get('median'),
        'tflops': perf_run.get('tflops'),
        'correctness_passed': correctness_passed,
        'summary_json': repo_rel(summary_path),
        'ncu_summary_json': repo_rel(run_dir / 'ncu_summary.json') if (run_dir / 'ncu_summary.json').exists() else None,
        'ncu_analysis_json': repo_rel(run_dir / 'ncu_analysis.json') if (run_dir / 'ncu_analysis.json').exists() else None,
        'ncu_analysis_md': repo_rel(run_dir / 'ncu_analysis.md') if (run_dir / 'ncu_analysis.md').exists() else None,
        'ncu_rep_path': repo_rel(run_dir / 'ncu_profile.ncu-rep') if (run_dir / 'ncu_profile.ncu-rep').exists() else None,
        'updated_at': now_local_iso(),
    }
    benchmark_state['updated_at'] = now_local_iso()
    write_json(BENCHMARK_STATE_PATH, benchmark_state)
    write_text(REPO_ROOT / 'state' / 'benchmark_baselines.md', render_benchmark_baselines_md(benchmark_state))
    refresh_all_views()


def main() -> None:
    args = parse_args()
    cmd = [
        sys.executable,
        str(Path('scripts') / 'eval_kernel.py'),
        '--runner', str(args.runner),
        '--kernel-tag', args.kernel_tag,
        '--config', str(args.config),
        '--dataset-root', str(args.dataset_root),
        '--runs-root', str(args.runs_root),
        '--flush-cache-mb', str(args.flush_cache_mb),
        '--ncu-bin', args.ncu_bin,
        '--ncu-metrics-file', str(args.ncu_metrics_file),
    ]

    if args.workdir is not None:
        cmd += ['--workdir', str(args.workdir)]
    if args.warmup is not None:
        cmd += ['--warmup', str(args.warmup)]
    if args.iters is not None:
        cmd += ['--iters', str(args.iters)]
    if args.skip_ncu:
        cmd += ['--skip-ncu']

    for item in args.extra_runner_arg:
        cmd.append(f'--extra-runner-arg={item}')

    with gpu_exclusive(reason=f'cublas_baseline:{args.kernel_tag}'):
        proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if proc.stdout:
        print(proc.stdout, end='')
    if proc.stderr:
        print(proc.stderr, end='', file=sys.stderr)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)

    run_dir = parse_run_dir(proc.stdout)
    update_cublas_baseline(run_dir)
    print(f'[baseline] updated cuBLAS benchmark registry from {repo_rel(run_dir)}')


if __name__ == '__main__':
    main()
