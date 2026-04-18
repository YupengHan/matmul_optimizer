#!/usr/bin/env python3
"""
Thin wrapper around eval_kernel.py for the CUTLASS reference runner.

Usage example:
    python scripts/run_cutlass_baseline.py \
        --runner ./build/cutlass_runner \
        --kernel-tag cutlass_ref_v0

This wrapper exists mainly to make the pipeline naming explicit.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Run the CUTLASS baseline through eval_kernel.py')
    parser.add_argument('--runner', type=Path, required=True, help='CUTLASS benchmark runner binary or Python script')
    parser.add_argument('--kernel-tag', default='cutlass_ref', help='Kernel tag used in the run artifact directory')
    parser.add_argument('--config', type=Path, default=Path('configs/fixed_bf16_gemm_v1.json'))
    parser.add_argument('--dataset-root', type=Path, default=Path('artifacts/datasets'))
    parser.add_argument('--runs-root', type=Path, default=Path('runs'))
    parser.add_argument('--workdir', type=Path, default=None)
    parser.add_argument('--warmup', type=int, default=None)
    parser.add_argument('--iters', type=int, default=None)
    parser.add_argument('--flush-cache-mb', type=int, default=256)
    parser.add_argument('--skip-ncu', action='store_true')
    parser.add_argument('--extra-runner-arg', action='append', default=[], help='Extra arg appended to the CUTLASS runner; may be passed multiple times')
    return parser.parse_args()


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
        cmd += ['--extra-runner-arg', item]

    raise SystemExit(subprocess.run(cmd, check=False).returncode)


if __name__ == '__main__':
    main()
