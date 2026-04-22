#!/usr/bin/env python3
"""Cross-process GPU lock for the matmul_optimizer workflow.

Two agents (e.g. one Codex instance and one Claude instance) may share the
same physical GPU from isolated repo folders on the same machine. They avoid
stepping on each other by acquiring an exclusive ``fcntl.flock`` on a single
lock file located outside any repo, so both folders see the same lock.

Default lock path: ``$HOME/.cache/matmul_optimizer/gpu.lock``
Override with the env var ``MATMUL_GPU_LOCK``.

Agent identity (for observability only) comes from ``MATMUL_AGENT_ID``.

Usage (library):

    from gpu_lock import gpu_exclusive
    with gpu_exclusive(reason='node_a:bf16_gemm_v1'):
        subprocess.run([...])  # runner + ncu

Usage (CLI):

    python scripts/gpu_lock.py status
    python scripts/gpu_lock.py run -- python scripts/eval_kernel.py ...
"""

from __future__ import annotations

import contextlib
import fcntl
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterator, Optional, Sequence


def default_lock_path() -> Path:
    override = os.environ.get('MATMUL_GPU_LOCK')
    if override:
        return Path(override)
    return Path.home() / '.cache' / 'matmul_optimizer' / 'gpu.lock'


def _holder_path(lock_path: Path) -> Path:
    return lock_path.with_name(lock_path.name + '.holder')


def _agent_id() -> str:
    return os.environ.get('MATMUL_AGENT_ID', 'unknown')


def _write_holder(lock_path: Path, reason: Optional[str]) -> None:
    payload = {
        'pid': os.getpid(),
        'agent_id': _agent_id(),
        'cwd': os.getcwd(),
        'reason': reason,
        'started_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
    }
    try:
        _holder_path(lock_path).write_text(
            json.dumps(payload, indent=2) + '\n', encoding='utf-8'
        )
    except OSError:
        pass


def _clear_holder(lock_path: Path) -> None:
    try:
        _holder_path(lock_path).unlink()
    except FileNotFoundError:
        pass
    except OSError:
        pass


def read_holder(lock_path: Optional[Path] = None) -> Optional[dict]:
    path = _holder_path(lock_path or default_lock_path())
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return None


@contextlib.contextmanager
def gpu_exclusive(
    reason: Optional[str] = None,
    lock_path: Optional[Path] = None,
    heartbeat_seconds: int = 30,
) -> Iterator[None]:
    """Block until the GPU lock is free, then hold it exclusively."""
    lock = lock_path or default_lock_path()
    lock.parent.mkdir(parents=True, exist_ok=True)
    handle = lock.open('a+')
    acquired = False
    waited = 0
    try:
        while not acquired:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
            except BlockingIOError:
                holder = read_holder(lock) or {}
                print(
                    f'[gpu_lock] waiting {waited}s for GPU '
                    f'(holder pid={holder.get("pid", "?")} '
                    f'agent={holder.get("agent_id", "?")} '
                    f'since={holder.get("started_at", "?")} '
                    f'reason={holder.get("reason", "?")})',
                    file=sys.stderr,
                    flush=True,
                )
                time.sleep(heartbeat_seconds)
                waited += heartbeat_seconds
        _write_holder(lock, reason)
        if waited:
            print(
                f'[gpu_lock] acquired after {waited}s (agent={_agent_id()} reason={reason})',
                file=sys.stderr,
                flush=True,
            )
        yield
    finally:
        if acquired:
            _clear_holder(lock)
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            except OSError:
                pass
        handle.close()


def _cli_status() -> int:
    lock = default_lock_path()
    holder = read_holder(lock)
    if holder is None:
        print(f'[gpu_lock] free (lock file: {lock})')
        return 0
    print(
        f'[gpu_lock] held by pid={holder.get("pid")} '
        f'agent={holder.get("agent_id")} '
        f'since={holder.get("started_at")} '
        f'reason={holder.get("reason")}'
    )
    print(f'cwd: {holder.get("cwd")}')
    print(f'lock file: {lock}')
    return 0


def _cli_run(argv: Sequence[str]) -> int:
    if not argv:
        print('usage: gpu_lock.py run -- <cmd> [args...]', file=sys.stderr)
        return 2
    if argv[0] == '--':
        argv = argv[1:]
    if not argv:
        print('usage: gpu_lock.py run -- <cmd> [args...]', file=sys.stderr)
        return 2
    reason = os.environ.get('MATMUL_GPU_LOCK_REASON') or ' '.join(argv[:2])
    with gpu_exclusive(reason=reason):
        proc = subprocess.run(argv)
    return proc.returncode


def main(argv: Sequence[str]) -> int:
    if not argv or argv[0] in ('-h', '--help'):
        print('usage: gpu_lock.py {status|run -- <cmd> [args...]}')
        return 0
    if argv[0] == 'status':
        return _cli_status()
    if argv[0] == 'run':
        return _cli_run(argv[1:])
    print(f'unknown subcommand: {argv[0]}', file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
