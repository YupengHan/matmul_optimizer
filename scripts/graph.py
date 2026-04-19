#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

import eval_kernel
from state_lib import (
    ACTIVE_DIRECTION_PATH,
    BENCHMARK_STATE_PATH,
    DIAGNOSIS_HISTORY_PATH,
    DOCS_DIR,
    GRAPH_STATE_PATH,
    LATEST_DIAGNOSIS_PATH,
    LATEST_NCU_SUMMARY_PATH,
    LATEST_RUN_PATH,
    REPO_ROOT,
    ROUND_HISTORY_PATH,
    ROUND_LOOP_STATE_PATH,
    RUN_REGISTRY_PATH,
    RUNS_DIR,
    STATE_DIR,
    SUPERVISOR_TASK_PATH,
    append_jsonl,
    current_kernel_path,
    default_active_direction,
    default_latest_diagnosis,
    default_round_loop_state,
    direction_lookup,
    ensure_machine_state,
    load_active_direction,
    load_benchmark_state,
    load_graph_state,
    load_latest_diagnosis,
    load_latest_ncu_summary,
    load_latest_run,
    load_round_loop_state,
    load_supervisor_task,
    now_local_iso,
    ordered_direction_ids,
    repo_rel,
    timestamp_tag,
    write_json,
    write_text,
)

LATEST_RUN_MD_PATH = STATE_DIR / 'latest_run.md'
LATEST_NCU_SUMMARY_MD_PATH = STATE_DIR / 'latest_ncu_summary.md'
NODE_B_CONTEXT_PATH = STATE_DIR / 'node_b_context.md'
NODE_C_CONTEXT_PATH = STATE_DIR / 'node_c_context.md'
PROGRESS_MD_PATH = STATE_DIR / 'progress.md'
CURRENT_FOCUS_MD_PATH = STATE_DIR / 'current_focus.md'
HUMAN_REVIEW_MD_PATH = STATE_DIR / 'human_review.md'
BENCHMARK_BASELINES_MD_PATH = STATE_DIR / 'benchmark_baselines.md'
ROUNDS_MD_PATH = STATE_DIR / 'rounds.md'
NODE_A_BUILD_LOG_PATH = STATE_DIR / 'node_a_last_build.log'
NODE_C_BUILD_LOG_PATH = STATE_DIR / 'node_c_last_build.log'
SUPERVISOR_CONTEXT_MD_PATH = STATE_DIR / 'supervisor_context.md'
SWEEP_FIXED_MAIN_TILES_PATH = REPO_ROOT / 'scripts' / 'sweep_fixed_main_tiles.py'

ALLOWED_NODE_C_PATHS = [
    REPO_ROOT / 'src' / 'kernels',
    REPO_ROOT / 'src' / 'runner' / 'main.cpp',
    REPO_ROOT / 'include',
    REPO_ROOT / 'CMakeLists.txt',
    REPO_ROOT / 'scripts' / 'graph.py',
    SWEEP_FIXED_MAIN_TILES_PATH,
]


def fmt_value(value: Any, suffix: str = '') -> str:
    if value is None:
        return 'N/A'
    if isinstance(value, float):
        return f'{value:.6f}{suffix}'
    return f'{value}{suffix}'


def fmt_runtime(value: Any) -> str:
    if value is None:
        return 'N/A'
    return f'{float(value):.6f} ms'


def fmt_tflops(value: Any) -> str:
    if value is None:
        return 'N/A'
    return f'{float(value):.6f} TFLOP/s'


def active_round_index(round_loop: Dict[str, Any]) -> Optional[int]:
    if round_loop.get('current_round_index') is not None:
        return int(round_loop['current_round_index'])
    if round_loop.get('active') and round_loop.get('remaining_rounds', 0) > 0:
        return int(round_loop.get('next_round_index', 1))
    return None


def round_label(round_loop: Dict[str, Any]) -> str:
    idx = active_round_index(round_loop)
    total = round_loop.get('total_rounds')
    if idx is None or not total:
        return 'single-run'
    return f'round {idx}/{total}'


def compute_perf_delta(previous_run: Dict[str, Any], latest_run: Dict[str, Any]) -> tuple[Optional[float], Optional[float], str]:
    prev_runtime = previous_run.get('median_runtime_ms')
    curr_runtime = latest_run.get('median_runtime_ms')
    prev_tflops = previous_run.get('tflops')
    curr_tflops = latest_run.get('tflops')
    if prev_runtime is None or curr_runtime is None:
        return None, None, 'unknown'
    runtime_delta = float(curr_runtime) - float(prev_runtime)
    tflops_delta = None
    if prev_tflops is not None and curr_tflops is not None:
        tflops_delta = float(curr_tflops) - float(prev_tflops)
    if runtime_delta < 0:
        verdict = 'improved'
    elif runtime_delta > 0:
        verdict = 'regressed'
    else:
        verdict = 'flat'
    return runtime_delta, tflops_delta, verdict


def fmt_delta_ms(value: Optional[float]) -> str:
    if value is None:
        return 'N/A'
    return f'{value:+.6f} ms'


def fmt_delta_tflops(value: Optional[float]) -> str:
    if value is None:
        return 'N/A'
    return f'{value:+.6f} TFLOP/s'


def print_step(message: str) -> None:
    print(f'[graph] {message}')


def run_command(
    cmd: Sequence[str],
    *,
    cwd: Path = REPO_ROOT,
    capture: bool = False,
    check: bool = False,
    stdin_text: Optional[str] = None,
) -> subprocess.CompletedProcess[str]:
    print_step(f'$ {shlex.join(list(cmd))}')
    return subprocess.run(
        list(cmd),
        cwd=str(cwd),
        text=True,
        input=stdin_text,
        capture_output=capture,
        check=check,
    )


def running_inside_codex_sandbox() -> bool:
    try:
        init_cmdline = (Path('/proc/1/cmdline').read_bytes().replace(b'\x00', b' ')).decode('utf-8', errors='ignore')
    except OSError:
        return False
    return 'codex-linux-sandbox' in init_cmdline


def ensure_node_a_can_access_gpu() -> None:
    if running_inside_codex_sandbox():
        raise RuntimeError(
            'node_a must run outside the Codex sandbox because it requires direct CUDA / Nsight Compute access; '
            'rerun `python scripts/graph.py node_a` with escalated permissions.'
        )


def git_output(args: Sequence[str]) -> str:
    proc = run_command(['git', *args], capture=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f'git {" ".join(args)} failed')
    return proc.stdout.strip()


def git_optional_output(args: Sequence[str]) -> Optional[str]:
    proc = run_command(['git', *args], capture=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def relative_paths(paths: Iterable[Path | str]) -> List[str]:
    return [repo_rel(Path(path)) or str(path) for path in paths]


def path_is_allowed(rel_path: str, allowlist: Sequence[Path | str]) -> bool:
    rel = Path(rel_path)
    for allowed in allowlist:
        allowed_rel = Path(repo_rel(Path(allowed)) or str(allowed))
        if rel == allowed_rel:
            return True
        try:
            rel.relative_to(allowed_rel)
            return True
        except ValueError:
            continue
    return False


def ensure_no_unrelated_staged_changes(allowlist: Sequence[Path | str]) -> None:
    staged = git_optional_output(['diff', '--cached', '--name-only'])
    staged_paths = [line.strip() for line in (staged or '').splitlines() if line.strip()]
    unrelated = [path for path in staged_paths if not path_is_allowed(path, allowlist)]
    if unrelated:
        raise RuntimeError(
            'refusing automatic commit because unrelated staged changes already exist: '
            + ', '.join(unrelated)
        )


def git_has_staged_changes(allowlist: Sequence[Path | str]) -> bool:
    rels = relative_paths(allowlist)
    proc = run_command(['git', 'diff', '--cached', '--quiet', '--', *rels], capture=False)
    return proc.returncode == 1


def stage_paths(paths: Sequence[Path | str]) -> None:
    rels = relative_paths(paths)
    if rels:
        run_command(['git', 'add', '--', *rels], check=True)


def commit_paths(paths: Sequence[Path | str], message: str) -> Optional[str]:
    ensure_no_unrelated_staged_changes(paths)
    stage_paths(paths)
    if not git_has_staged_changes(paths):
        print_step('no staged changes for this node; skipping commit')
        return None
    run_command(['git', 'commit', '-F', '-'], stdin_text=message, check=True)
    return git_output(['rev-parse', 'HEAD'])


def list_tracked_paths(ref: Optional[str], scope_paths: Sequence[Path | str]) -> List[str]:
    rels = relative_paths(scope_paths)
    if ref is None:
        proc = run_command(['git', 'ls-files', '--', *rels], capture=True)
    else:
        proc = run_command(['git', 'ls-tree', '-r', '--name-only', ref, '--', *rels], capture=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or 'failed to list tracked paths')
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def restore_paths_from_commit(source_commit: str, scope_paths: Sequence[Path | str]) -> List[Path]:
    current_paths = set(list_tracked_paths(None, scope_paths))
    source_paths = set(list_tracked_paths(source_commit, scope_paths))
    changed: List[Path] = []

    for rel_path in sorted(current_paths | source_paths):
        target_path = REPO_ROOT / rel_path
        if rel_path in source_paths:
            show = run_command(['git', 'show', f'{source_commit}:{rel_path}'], capture=True)
            if show.returncode != 0:
                raise RuntimeError(show.stderr.strip() or f'failed to read {rel_path} from {source_commit}')
            new_text = show.stdout
            old_text = target_path.read_text(encoding='utf-8') if target_path.exists() else None
            if old_text != new_text:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(new_text, encoding='utf-8')
                changed.append(target_path)
        elif target_path.exists():
            target_path.unlink()
            changed.append(target_path)

    return changed


def candidate_build_inputs() -> List[Path]:
    watched: List[Path] = [REPO_ROOT / 'CMakeLists.txt']
    watched.extend(sorted((REPO_ROOT / 'include').glob('**/*')))
    watched.extend(sorted((REPO_ROOT / 'src' / 'runner').glob('**/*')))
    watched.extend(sorted((REPO_ROOT / 'src' / 'kernels').glob('**/*')))
    return [path for path in watched if path.is_file()]


def needs_rebuild(binary_path: Path) -> bool:
    if not binary_path.exists():
        return True
    binary_mtime = binary_path.stat().st_mtime
    for path in candidate_build_inputs():
        if path.stat().st_mtime > binary_mtime:
            return True
    return False


def maybe_run_build(binary_path: Path, *, force: bool, log_path: Path) -> bool:
    if not force and not needs_rebuild(binary_path):
        print_step(f'skipping build; {repo_rel(binary_path)} is newer than watched inputs')
        return True

    configure = run_command(
        ['cmake', '-S', '.', '-B', 'build', '-DENABLE_CUTLASS_RUNNER=OFF'],
        capture=True,
    )
    build = run_command(['cmake', '--build', 'build', '-j', '4'], capture=True)
    combined = textwrap.dedent(
        f'''\
        $ cmake -S . -B build -DENABLE_CUTLASS_RUNNER=OFF
        {configure.stdout}
        {configure.stderr}

        $ cmake --build build -j 4
        {build.stdout}
        {build.stderr}
        '''
    )
    write_text(log_path, combined)
    return configure.returncode == 0 and build.returncode == 0


def head_commit() -> Optional[str]:
    return git_optional_output(['rev-parse', 'HEAD'])


def short_head() -> Optional[str]:
    return git_optional_output(['rev-parse', '--short', 'HEAD'])


def default_kernel_tag(kernel_path: str) -> str:
    stem = Path(kernel_path).stem
    short = short_head()
    return f'{stem}_{short}' if short else stem


def parse_run_dir_from_stdout(stdout: str) -> Path:
    marker = '[done] wrote run artifacts to '
    for line in stdout.splitlines():
        if marker in line:
            return (REPO_ROOT / line.split(marker, 1)[1].strip()).resolve()
    raise RuntimeError('failed to locate run directory from eval_kernel.py output')


def load_json_file(path: Path) -> Dict[str, Any]:
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def summarize_run(
    run_dir: Path,
    measured_commit: Optional[str],
    benchmark_state: Dict[str, Any],
) -> tuple[Dict[str, Any], Dict[str, Any], bool]:
    raw_summary = load_json_file(run_dir / 'summary.json')
    ncu_summary_path = run_dir / 'ncu_summary.json'
    if ncu_summary_path.exists():
        raw_ncu = load_json_file(ncu_summary_path)
    else:
        csv_path = run_dir / 'ncu_metrics.csv'
        metrics = {}
        if csv_path.exists():
            metrics = eval_kernel.pick_headline_metrics(
                eval_kernel.parse_ncu_csv(csv_path),
                eval_kernel.read_metrics_file(REPO_ROOT / 'configs' / 'ncu_metrics_core.txt'),
            )
        raw_ncu = {
            'status': 'available' if metrics else 'missing',
            'headline_metrics': metrics,
            'raw_csv_path': repo_rel(csv_path) if csv_path.exists() else None,
            'raw_rep_path': repo_rel(run_dir / 'ncu_profile.ncu-rep'),
            'raw_details_csv_path': repo_rel(run_dir / 'ncu_details.csv') if (run_dir / 'ncu_details.csv').exists() else None,
        }

    correctness_runs = raw_summary.get('correctness_runs', [])
    passed_cases = sum(1 for item in correctness_runs if item.get('passed'))
    correctness_passed = bool(correctness_runs) and passed_cases == len(correctness_runs)
    perf = raw_summary.get('perf_run') or {}
    perf_runtime = perf.get('runtime_ms') or {}
    run_id = run_dir.name

    current_best = (benchmark_state.get('best_custom') or {}).get('median_runtime_ms')
    candidate_runtime = perf_runtime.get('median')
    is_new_best = bool(
        correctness_passed
        and perf.get('passed')
        and candidate_runtime is not None
        and (current_best is None or float(candidate_runtime) < float(current_best))
    )

    latest_run = {
        'run_id': run_id,
        'run_dir': repo_rel(run_dir),
        'raw_summary_json': repo_rel(run_dir / 'summary.json'),
        'raw_summary_md': repo_rel(run_dir / 'summary.md'),
        'kernel_tag': raw_summary.get('kernel_tag'),
        'runner': raw_summary.get('runner'),
        'dataset_id': raw_summary.get('dataset_id'),
        'benchmark_case': raw_summary.get('benchmark_case'),
        'correctness_passed': correctness_passed,
        'correctness_cases_total': len(correctness_runs),
        'correctness_cases_passed': passed_cases,
        'perf_passed': perf.get('passed'),
        'median_runtime_ms': perf_runtime.get('median'),
        'p10_runtime_ms': perf_runtime.get('p10'),
        'p90_runtime_ms': perf_runtime.get('p90'),
        'tflops': perf.get('tflops'),
        'ncu_rep_path': repo_rel(run_dir / 'ncu_profile.ncu-rep') if (run_dir / 'ncu_profile.ncu-rep').exists() else None,
        'ncu_csv_path': repo_rel(run_dir / 'ncu_metrics.csv') if (run_dir / 'ncu_metrics.csv').exists() else None,
        'ncu_summary_json': repo_rel(LATEST_NCU_SUMMARY_PATH),
        'is_new_best_custom': is_new_best,
        'measured_commit': measured_commit,
        'generated_at': now_local_iso(),
    }

    latest_ncu = {
        'status': raw_ncu.get('status', 'missing'),
        'source_run_id': run_id,
        'source_run_dir': repo_rel(run_dir),
        'kernel_name': raw_ncu.get('kernel_name'),
        'block_size': raw_ncu.get('block_size'),
        'grid_size': raw_ncu.get('grid_size'),
        'registers_per_thread': raw_ncu.get('registers_per_thread'),
        'shared_mem_per_block_allocated': raw_ncu.get('shared_mem_per_block_allocated'),
        'headline_metrics': raw_ncu.get('headline_metrics', {}),
        'raw_csv_path': repo_rel(run_dir / 'ncu_metrics.csv') if (run_dir / 'ncu_metrics.csv').exists() else None,
        'raw_rep_path': repo_rel(run_dir / 'ncu_profile.ncu-rep') if (run_dir / 'ncu_profile.ncu-rep').exists() else None,
        'raw_details_csv_path': (
            repo_rel(run_dir / Path(raw_ncu['raw_details_csv_path']).name)
            if raw_ncu.get('raw_details_csv_path')
            else (repo_rel(run_dir / 'ncu_details.csv') if (run_dir / 'ncu_details.csv').exists() else None)
        ),
        'generated_at': now_local_iso(),
    }
    return latest_run, latest_ncu, is_new_best


def update_best_custom(benchmark_state: Dict[str, Any], latest_run: Dict[str, Any]) -> None:
    benchmark_state['best_custom'] = {
        'run_id': latest_run.get('run_id'),
        'run_dir': latest_run.get('run_dir'),
        'kernel_tag': latest_run.get('kernel_tag'),
        'median_runtime_ms': latest_run.get('median_runtime_ms'),
        'tflops': latest_run.get('tflops'),
        'correctness_passed': latest_run.get('correctness_passed'),
        'measured_commit': latest_run.get('measured_commit'),
        'summary_json': latest_run.get('raw_summary_json'),
        'ncu_summary_json': latest_run.get('ncu_summary_json'),
        'updated_at': now_local_iso(),
    }
    benchmark_state['updated_at'] = now_local_iso()


def compute_gap(benchmark_state: Dict[str, Any]) -> tuple[Optional[float], Optional[float]]:
    cutlass = benchmark_state.get('cutlass_baseline') or {}
    custom = benchmark_state.get('best_custom') or {}
    cutlass_runtime = cutlass.get('median_runtime_ms')
    custom_runtime = custom.get('median_runtime_ms')
    if cutlass_runtime is None or custom_runtime is None:
        return None, None
    absolute = float(custom_runtime) - float(cutlass_runtime)
    ratio = float(custom_runtime) / float(cutlass_runtime) if float(cutlass_runtime) else None
    return absolute, ratio


def direction_summary_line(direction: Dict[str, Any]) -> str:
    name = direction.get('name') or 'PENDING'
    bottleneck = direction.get('expected_bottleneck') or 'PENDING'
    return (
        f"{direction.get('direction_id', 'dir_xx')}: "
        f"{name} | "
        f"bottleneck: {bottleneck}"
    )


def render_latest_run_md(latest_run: Dict[str, Any]) -> str:
    lines = ['# Latest run', '']
    lines.append(f"- run id: `{latest_run.get('run_id', 'N/A')}`")
    lines.append(f"- run dir: `{latest_run.get('run_dir', 'N/A')}`")
    lines.append(f"- kernel tag: `{latest_run.get('kernel_tag', 'N/A')}`")
    lines.append(f"- round label: `{latest_run.get('round_label', 'single-run')}`")
    lines.append(f"- runner: `{latest_run.get('runner', 'N/A')}`")
    lines.append(f"- correctness: `{'PASS' if latest_run.get('correctness_passed') else 'FAIL' if latest_run.get('correctness_passed') is not None else 'N/A'}`")
    lines.append(
        f"- correctness cases: `{latest_run.get('correctness_cases_passed', 0)}/{latest_run.get('correctness_cases_total', 0)}`"
    )
    lines.append(f"- perf status: `{'PASS' if latest_run.get('perf_passed') else 'FAIL' if latest_run.get('perf_passed') is not None else 'N/A'}`")
    lines.append(f"- median runtime: `{fmt_runtime(latest_run.get('median_runtime_ms'))}`")
    lines.append(f"- p10 runtime: `{fmt_runtime(latest_run.get('p10_runtime_ms'))}`")
    lines.append(f"- p90 runtime: `{fmt_runtime(latest_run.get('p90_runtime_ms'))}`")
    lines.append(f"- TFLOP/s: `{fmt_tflops(latest_run.get('tflops'))}`")
    lines.append(f"- previous run id: `{latest_run.get('previous_run_id', 'N/A')}`")
    lines.append(f"- runtime delta vs previous measured run: `{fmt_delta_ms(latest_run.get('runtime_delta_ms'))}`")
    lines.append(f"- TFLOP/s delta vs previous measured run: `{fmt_delta_tflops(latest_run.get('tflops_delta'))}`")
    lines.append(f"- perf verdict: `{latest_run.get('perf_verdict', 'N/A')}`")
    lines.append(f"- implemented direction id: `{latest_run.get('implemented_direction_id', 'N/A')}`")
    lines.append(f"- implemented direction name: `{latest_run.get('implemented_direction_name', 'N/A')}`")
    lines.append(f"- implemented selection mode: `{latest_run.get('implemented_selection_mode', 'N/A')}`")
    lines.append(f"- implemented idea origin: `{latest_run.get('implemented_idea_origin', 'N/A')}`")
    lines.append(f"- raw summary json: `{latest_run.get('raw_summary_json', 'N/A')}`")
    lines.append(f"- measured commit: `{latest_run.get('measured_commit', 'N/A')}`")
    lines.append(f"- new best custom: `{'yes' if latest_run.get('is_new_best_custom') else 'no'}`")
    lines.append(f"- generated at: `{latest_run.get('generated_at', 'N/A')}`")
    return '\n'.join(lines) + '\n'


def render_latest_ncu_md(ncu_summary: Dict[str, Any]) -> str:
    lines = ['# Latest Nsight Compute summary', '']
    lines.append(f"- source run id: `{ncu_summary.get('source_run_id', 'N/A')}`")
    lines.append(f"- source run dir: `{ncu_summary.get('source_run_dir', 'N/A')}`")
    lines.append(f"- status: `{ncu_summary.get('status', 'unknown')}`")
    lines.append(f"- kernel name: `{ncu_summary.get('kernel_name', 'N/A')}`")
    lines.append(f"- block size: `{ncu_summary.get('block_size', 'N/A')}`")
    lines.append(f"- grid size: `{ncu_summary.get('grid_size', 'N/A')}`")
    lines.append(f"- registers / thread: `{ncu_summary.get('registers_per_thread', 'N/A')}`")
    lines.append(f"- shared mem / block allocated: `{ncu_summary.get('shared_mem_per_block_allocated', 'N/A')}`")
    lines.append(f"- raw csv path: `{ncu_summary.get('raw_csv_path', 'N/A')}`")
    lines.append(f"- raw rep path: `{ncu_summary.get('raw_rep_path', 'N/A')}`")
    lines.append(f"- raw detailed csv path: `{ncu_summary.get('raw_details_csv_path', 'N/A')}`")
    lines.append('')
    lines.append('## Headline metrics')
    lines.append('')
    headline_metrics = ncu_summary.get('headline_metrics') or {}
    if not headline_metrics:
        lines.append('No parsed headline metrics are available yet.')
    else:
        for key, value in headline_metrics.items():
            lines.append(f"- `{key}`: `{value}`")
    return '\n'.join(lines) + '\n'


def render_benchmark_baselines_md(benchmark_state: Dict[str, Any]) -> str:
    cutlass = benchmark_state.get('cutlass_baseline') or {}
    custom = benchmark_state.get('best_custom') or {}
    absolute_gap, runtime_ratio = compute_gap(benchmark_state)

    lines = ['# Benchmark baselines', '', '## Official benchmark', '']
    lines.append(f"- dataset: `{benchmark_state.get('dataset_id', 'fixed_bf16_gemm_v1')}`")
    lines.append(f"- metric of record: `{benchmark_state.get('metric_of_record', 'median_runtime_ms')}`")
    lines.append('- correctness must pass before a performance result is accepted')
    lines.append('')
    lines.append('## CUTLASS baseline')
    lines.append('')
    if not cutlass:
        lines.append('- status: NOT RECORDED')
    else:
        lines.append(f"- status: RECORDED")
        lines.append(f"- kernel tag: `{cutlass.get('kernel_tag', 'N/A')}`")
        lines.append(f"- runtime: `{fmt_runtime(cutlass.get('median_runtime_ms'))}`")
        lines.append(f"- TFLOP/s: `{fmt_tflops(cutlass.get('tflops'))}`")
        lines.append(f"- correctness: `{'PASS' if cutlass.get('correctness_passed') else 'FAIL'}`")
        lines.append(f"- run dir: `{cutlass.get('run_dir', 'N/A')}`")
        lines.append(f"- summary json: `{cutlass.get('summary_json', 'N/A')}`")
    lines.append('')
    lines.append('## Best custom kernel')
    lines.append('')
    if not custom:
        lines.append('- status: NOT RECORDED')
    else:
        lines.append('- status: RECORDED')
        lines.append(f"- kernel tag: `{custom.get('kernel_tag', 'N/A')}`")
        lines.append(f"- runtime: `{fmt_runtime(custom.get('median_runtime_ms'))}`")
        lines.append(f"- TFLOP/s: `{fmt_tflops(custom.get('tflops'))}`")
        lines.append(f"- correctness: `{'PASS' if custom.get('correctness_passed') else 'FAIL'}`")
        lines.append(f"- run dir: `{custom.get('run_dir', 'N/A')}`")
        lines.append(f"- summary json: `{custom.get('summary_json', 'N/A')}`")
        lines.append(f"- measured commit: `{custom.get('measured_commit', 'N/A')}`")
    lines.append('')
    lines.append('## Gap')
    lines.append('')
    if absolute_gap is None or runtime_ratio is None:
        lines.append('- gap: NOT AVAILABLE YET')
    else:
        lines.append(f"- absolute runtime gap: `{absolute_gap:.6f} ms`")
        lines.append(f"- runtime ratio: `{runtime_ratio:.6f}x` slower than CUTLASS")
    return '\n'.join(lines) + '\n'


def render_rounds_md(round_loop: Dict[str, Any]) -> str:
    lines = ['# Round loop', '']
    lines.append(f"- active: `{'yes' if round_loop.get('active') else 'no'}`")
    lines.append(f"- status: `{round_loop.get('status', 'idle')}`")
    lines.append(f"- total rounds: `{round_loop.get('total_rounds', 0)}`")
    lines.append(f"- completed rounds: `{round_loop.get('completed_rounds', 0)}`")
    lines.append(f"- remaining rounds: `{round_loop.get('remaining_rounds', 0)}`")
    lines.append(f"- current round label: `{round_label(round_loop)}`")
    lines.append(f"- auto use recommended: `{'yes' if round_loop.get('auto_use_recommended') else 'no'}`")
    lines.append(f"- accepted base run id: `{round_loop.get('accepted_base_run_id', 'N/A')}`")
    lines.append(f"- accepted base measured commit: `{round_loop.get('accepted_base_measured_commit', 'N/A')}`")
    lines.append(f"- accepted base runtime: `{fmt_runtime(round_loop.get('accepted_base_runtime_ms'))}`")
    lines.append(f"- started at: `{round_loop.get('started_at', 'N/A')}`")
    lines.append(f"- completed at: `{round_loop.get('completed_at', 'N/A')}`")
    lines.append(f"- history path: `{round_loop.get('history_path', repo_rel(ROUND_HISTORY_PATH))}`")
    lines.append(f"- notes: `{round_loop.get('notes', 'N/A')}`")
    last_round = round_loop.get('last_completed_round')
    lines.append('')
    lines.append('## Last completed round')
    lines.append('')
    if not last_round:
        lines.append('- no completed round recorded yet')
    else:
        lines.append(f"- round: `{last_round.get('round_index', 'N/A')}/{last_round.get('total_rounds', 'N/A')}`")
        lines.append(f"- direction: `{last_round.get('direction_id', 'N/A')}`")
        lines.append(f"- direction name: `{last_round.get('direction_name', 'N/A')}`")
        lines.append(f"- verdict: `{last_round.get('perf_verdict', 'N/A')}`")
        lines.append(f"- runtime delta: `{fmt_delta_ms(last_round.get('runtime_delta_ms'))}`")
        lines.append(f"- TFLOP/s delta: `{fmt_delta_tflops(last_round.get('tflops_delta'))}`")
        lines.append(f"- run dir: `{last_round.get('run_dir', 'N/A')}`")
        lines.append(f"- ncu rep path: `{last_round.get('ncu_rep_path', 'N/A')}`")
    return '\n'.join(lines) + '\n'


def render_progress_md(
    graph_state: Dict[str, Any],
    latest_run: Dict[str, Any],
    diagnosis: Dict[str, Any],
    active_direction: Dict[str, Any],
    benchmark_state: Dict[str, Any],
    round_loop: Dict[str, Any],
) -> str:
    cutlass = benchmark_state.get('cutlass_baseline') or {}
    absolute_gap, runtime_ratio = compute_gap(benchmark_state)
    lines = ['# Progress', '', '## Objective', '']
    lines.append('Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.')
    lines.append('')
    lines.append('## Workflow state')
    lines.append('')
    lines.append(f"- next node: `{graph_state.get('current_node', 'node_a')}`")
    lines.append(f"- previous node: `{graph_state.get('previous_node', 'N/A')}`")
    lines.append(f"- status: `{graph_state.get('status', 'unknown')}`")
    lines.append(f"- current kernel path: `{graph_state.get('current_kernel_path', current_kernel_path())}`")
    lines.append(f"- latest measured commit: `{graph_state.get('latest_commit', 'N/A')}`")
    lines.append(f"- plateau counter: `{graph_state.get('plateau_counter', 0)}`")
    lines.append(f"- round loop: `{round_label(round_loop)}`")
    lines.append(f"- rounds remaining: `{round_loop.get('remaining_rounds', 0)}`")
    lines.append(f"- notes: `{graph_state.get('notes', 'N/A')}`")
    lines.append('')
    lines.append('## Latest measured custom run')
    lines.append('')
    lines.append(f"- run id: `{latest_run.get('run_id', 'N/A')}`")
    lines.append(f"- run dir: `{latest_run.get('run_dir', 'N/A')}`")
    lines.append(f"- correctness: `{'PASS' if latest_run.get('correctness_passed') else 'FAIL' if latest_run.get('correctness_passed') is not None else 'N/A'}`")
    lines.append(f"- median runtime: `{fmt_runtime(latest_run.get('median_runtime_ms'))}`")
    lines.append(f"- TFLOP/s: `{fmt_tflops(latest_run.get('tflops'))}`")
    lines.append(f"- latest run summary: `{repo_rel(LATEST_RUN_PATH)}`")
    lines.append(f"- latest NCU summary: `{repo_rel(LATEST_NCU_SUMMARY_PATH)}`")
    if latest_run.get('is_new_best_custom'):
        lines.append('- result: `NEW BEST CUSTOM RUN`')
    lines.append('')
    lines.append('## Latest diagnosis state')
    lines.append('')
    lines.append(f"- diagnosis status: `{diagnosis.get('status', 'pending_generation')}`")
    lines.append(f"- diagnosis id: `{diagnosis.get('diagnosis_id', 'N/A')}`")
    lines.append(f"- recommended direction: `{diagnosis.get('recommended_direction_id', 'N/A')}`")
    lines.append(f"- approved direction: `{diagnosis.get('approved_direction_id', 'N/A')}`")
    lines.append(f"- diagnosis notes: `{diagnosis.get('notes', 'N/A')}`")
    if diagnosis.get('directions'):
        for direction in diagnosis.get('directions', []):
            lines.append(f"- {direction_summary_line(direction)}")
    else:
        lines.append('- no directions recorded yet')
    lines.append('')
    lines.append('## Active implementation direction')
    lines.append('')
    lines.append(f"- direction id: `{active_direction.get('direction_id', 'N/A')}`")
    lines.append(f"- selection mode: `{active_direction.get('selection_mode', 'N/A')}`")
    lines.append(f"- status: `{active_direction.get('status', 'idle')}`")
    lines.append(f"- notes: `{active_direction.get('notes', 'N/A')}`")
    lines.append('')
    lines.append('## Benchmark snapshot')
    lines.append('')
    lines.append(f"- CUTLASS median runtime: `{fmt_runtime(cutlass.get('median_runtime_ms'))}`")
    if absolute_gap is not None and runtime_ratio is not None:
        lines.append(f"- current best custom gap: `{absolute_gap:.6f} ms`, `{runtime_ratio:.6f}x` slower than CUTLASS")
    else:
        lines.append('- current best custom gap: `N/A`')
    return '\n'.join(lines) + '\n'


def render_current_focus_md(
    graph_state: Dict[str, Any],
    latest_run: Dict[str, Any],
    diagnosis: Dict[str, Any],
    active_direction: Dict[str, Any],
    round_loop: Dict[str, Any],
) -> str:
    lines = ['# Current focus', '']
    lines.append(f"- next node: `{graph_state.get('current_node', 'node_a')}`")
    lines.append(f"- status: `{graph_state.get('status', 'unknown')}`")
    lines.append(f"- latest run id: `{latest_run.get('run_id', 'N/A')}`")
    lines.append(f"- latest kernel tag: `{latest_run.get('kernel_tag', 'N/A')}`")
    lines.append(f"- median runtime: `{fmt_runtime(latest_run.get('median_runtime_ms'))}`")
    lines.append(f"- current kernel path: `{graph_state.get('current_kernel_path', current_kernel_path())}`")
    lines.append(f"- round loop: `{round_label(round_loop)}`")
    lines.append(f"- rounds remaining: `{round_loop.get('remaining_rounds', 0)}`")
    lines.append(f"- recommended direction: `{diagnosis.get('recommended_direction_id', 'N/A')}`")
    lines.append(f"- selected direction: `{active_direction.get('direction_id', 'N/A')}`")
    lines.append(f"- immediate next action: `{graph_state.get('notes', 'Run status to inspect the current node')}`")
    return '\n'.join(lines) + '\n'


def render_human_review_md(
    graph_state: Dict[str, Any],
    diagnosis: Dict[str, Any],
    active_direction: Dict[str, Any],
    round_loop: Dict[str, Any],
) -> str:
    lines = ['# Human review queue', '', '## Current workflow gate', '']
    lines.append(f"- next node: `{graph_state.get('current_node', 'node_a')}`")
    lines.append(f"- status: `{graph_state.get('status', 'unknown')}`")
    lines.append(f"- round loop: `{round_label(round_loop)}` with `{round_loop.get('remaining_rounds', 0)}` rounds remaining")
    lines.append('')
    lines.append('## Direction approval policy')
    lines.append('')
    lines.append('- explicit approval: `python scripts/graph.py approve --direction dir_02`')
    lines.append('- continue with recommended direction: `python scripts/graph.py use-recommended-direction`')
    lines.append('- node_c should implement exactly one selected direction')
    lines.append('')
    lines.append('## Latest diagnosis')
    lines.append('')
    lines.append(f"- diagnosis id: `{diagnosis.get('diagnosis_id', 'N/A')}`")
    lines.append(f"- diagnosis status: `{diagnosis.get('status', 'pending_generation')}`")
    lines.append(f"- recommended direction: `{diagnosis.get('recommended_direction_id', 'N/A')}`")
    lines.append(f"- approved direction: `{diagnosis.get('approved_direction_id', 'N/A')}`")
    lines.append(f"- diagnosis notes: `{diagnosis.get('notes', 'N/A')}`")
    if diagnosis.get('directions'):
        for direction in diagnosis.get('directions', []):
            lines.append(f"- {direction_summary_line(direction)}")
    else:
        lines.append('- no diagnosis recorded yet; run node_b first')
    lines.append('')
    lines.append('## Active direction')
    lines.append('')
    lines.append(f"- selected direction: `{active_direction.get('direction_id', 'N/A')}`")
    lines.append(f"- selection mode: `{active_direction.get('selection_mode', 'N/A')}`")
    lines.append(f"- status: `{active_direction.get('status', 'idle')}`")
    lines.append(f"- notes: `{active_direction.get('notes', 'N/A')}`")
    return '\n'.join(lines) + '\n'


def render_node_b_context(
    graph_state: Dict[str, Any],
    latest_run: Dict[str, Any],
    ncu_summary: Dict[str, Any],
    diagnosis: Dict[str, Any],
    round_loop: Dict[str, Any],
) -> str:
    autotune_paths = sorted(
        path for path in STATE_DIR.glob('autotune_*_main_tiles.*')
        if path.suffix in {'.json', '.md'}
    )
    autotune_lines = ''
    if autotune_paths:
        formatted = '\n'.join(f'- `{repo_rel(path)}`' for path in autotune_paths)
        autotune_lines = f'\n{formatted}\n'
    return textwrap.dedent(
        f'''\
        # Node B context

        Node B is the diagnosis node. Read the files below, then write exactly three directions to `state/latest_diagnosis.json`.

        ## Read order

        - `state/latest_run.md`
        - `state/latest_ncu_summary.md`
        - `docs/heuristics.md`
        - `state/progress.md`
        - `state/current_focus.md`
        - `state/human_review.md`
        - `{graph_state.get('current_kernel_path', current_kernel_path())}`
        - `{latest_run.get('raw_summary_json', 'N/A')}`
        - `{ncu_summary.get('raw_csv_path', 'N/A')}`
        - `{ncu_summary.get('raw_details_csv_path', 'N/A')}`
        - `{ncu_summary.get('raw_rep_path', 'N/A')}`
{autotune_lines if autotune_lines else ''}

        Use the raw detailed CSV when the headline summary is too shallow to explain pipeline, memory, or bank-conflict behavior.
        Use the autotune sweep summaries when present to anchor direction ranking in measured tile-width data instead of only one run snapshot.

        ## Output contract

        - write exactly 3 directions
        - preserve `direction_id` values `dir_01`, `dir_02`, `dir_03`
        - each direction must include:
          - `hypothesis`
          - `expected_bottleneck`
          - `code_locations`
          - `risk`
          - `metrics_to_recheck`
        - set `recommended_direction_id`
        - after editing the diagnosis file, run `python scripts/graph.py node_b --finalize`

        ## Current source snapshot

        - round loop: `{round_label(round_loop)}`
        - rounds remaining after this one: `{max(round_loop.get('remaining_rounds', 0) - 1, 0) if round_loop.get('active') else 0}`
        - latest run id: `{latest_run.get('run_id', 'N/A')}`
        - median runtime: `{fmt_runtime(latest_run.get('median_runtime_ms'))}`
        - TFLOP/s: `{fmt_tflops(latest_run.get('tflops'))}`
        - measured commit: `{latest_run.get('measured_commit', 'N/A')}`
        - existing diagnosis status: `{diagnosis.get('status', 'pending_generation')}`
        '''
    ).rstrip() + '\n'


def render_node_c_context(
    graph_state: Dict[str, Any],
    diagnosis: Dict[str, Any],
    active_direction: Dict[str, Any],
    dirty_paths: List[str],
    round_loop: Dict[str, Any],
) -> str:
    direction = direction_lookup(diagnosis, active_direction.get('direction_id') or '')
    direction_name = direction.get('name') if direction else None
    lines = ['# Node C context', '']
    lines.append('Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.')
    lines.append('')
    lines.append('## Selected direction')
    lines.append('')
    lines.append(f"- direction id: `{active_direction.get('direction_id', 'N/A')}`")
    lines.append(f"- direction name: `{direction_name or 'N/A'}`")
    lines.append(f"- selection mode: `{active_direction.get('selection_mode', 'N/A')}`")
    lines.append(f"- source diagnosis id: `{active_direction.get('source_diagnosis_id', 'N/A')}`")
    lines.append(f"- round loop: `{round_label(round_loop)}`")
    if direction:
        lines.append(f"- hypothesis: `{direction.get('hypothesis', 'N/A')}`")
        lines.append(f"- expected bottleneck: `{direction.get('expected_bottleneck', 'N/A')}`")
        lines.append(f"- code locations: `{', '.join(direction.get('code_locations', [])) or 'N/A'}`")
        lines.append(f"- risk: `{direction.get('risk', 'N/A')}`")
        lines.append(f"- metrics to re-check: `{', '.join(direction.get('metrics_to_recheck', [])) or 'N/A'}`")
    lines.append('')
    lines.append('## Allowed edit surface')
    lines.append('')
    lines.append('- `src/kernels/*`')
    lines.append('- `src/runner/main.cpp` when the direction requires runner glue')
    lines.append('- `include/*` when a stable interface change is required')
    lines.append('- `CMakeLists.txt` only if the build path genuinely needs it')
    lines.append('- `scripts/graph.py` or `scripts/sweep_fixed_main_tiles.py` only when the direction requires minimal workflow glue')
    lines.append('')
    lines.append('## Required commands')
    lines.append('')
    lines.append('- edit code for one direction only')
    lines.append('- then run `python scripts/graph.py node_c --finalize`')
    lines.append('- default behavior after a successful node_c finalize is to auto-run node_a')
    lines.append('')
    lines.append('## Dirty working tree snapshot before node_c finalize')
    lines.append('')
    if not active_direction.get('direction_id'):
        lines.append('- no active direction selected yet; select one before using the dirty-path guardrail')
    elif not dirty_paths:
        lines.append('- no tracked dirty paths at prepare time')
    else:
        for path in dirty_paths:
            lines.append(f"- `{path}`")
    return '\n'.join(lines) + '\n'


def compute_supervisor_task(
    graph_state: Dict[str, Any],
    diagnosis: Dict[str, Any],
    active_direction: Dict[str, Any],
    round_loop: Dict[str, Any],
) -> Dict[str, Any]:
    current_node = graph_state.get('current_node', 'node_a')
    task = {
        'supervisor_role': 'main_codex_agent',
        'dispatch_node': current_node,
        'dispatch_mode': 'direct_script',
        'graph_status': graph_state.get('status', 'unknown'),
        'round_label': round_label(round_loop),
        'round_loop_active': bool(round_loop.get('active')),
        'rounds_remaining': int(round_loop.get('remaining_rounds', 0)),
        'auto_use_recommended': bool(round_loop.get('auto_use_recommended')),
        'requires_gpu_access': False,
        'prepare_command': None,
        'selection_command': None,
        'finalize_command': None,
        'protocol_doc': 'docs/supervisor_protocol.md',
        'context_file': None,
        'active_direction_id': active_direction.get('direction_id'),
        'recommended_direction_id': diagnosis.get('recommended_direction_id'),
        'notes': graph_state.get('notes', 'Inspect graph_state.json and dispatch the next node.'),
    }

    if current_node == 'node_a':
        task.update(
            {
                'dispatch_mode': 'direct_script',
                'requires_gpu_access': True,
                'prepare_command': 'python scripts/graph.py node_a',
                'protocol_doc': 'AGENTS.md',
                'notes': 'Run node_a directly from the main Codex agent outside the sandbox, then re-read graph state.',
            }
        )
        return task

    if current_node == 'node_b':
        task.update(
            {
                'dispatch_mode': 'sub_agent',
                'prepare_command': 'python scripts/graph.py node_b',
                'finalize_command': 'python scripts/graph.py node_b --finalize',
                'protocol_doc': 'docs/node_b_protocol.md',
                'context_file': repo_rel(NODE_B_CONTEXT_PATH),
                'notes': 'Prepare node_b context if needed, spawn a diagnosis sub-agent, then finalize node_b from the main Codex agent.',
            }
        )
        return task

    if current_node == 'node_c':
        selection_command = None
        if not active_direction.get('direction_id'):
            if diagnosis.get('recommended_direction_id') and round_loop.get('auto_use_recommended'):
                selection_command = 'python scripts/graph.py use-recommended-direction'
            else:
                selection_command = 'python scripts/graph.py approve --direction dir_0X'
        task.update(
            {
                'dispatch_mode': 'sub_agent',
                'prepare_command': 'python scripts/graph.py node_c',
                'selection_command': selection_command,
                'finalize_command': 'python scripts/graph.py node_c --finalize',
                'protocol_doc': 'docs/node_c_protocol.md',
                'context_file': repo_rel(NODE_C_CONTEXT_PATH),
                'notes': 'Ensure exactly one direction is selected, spawn an implementation sub-agent, then finalize node_c from the main Codex agent.',
            }
        )
        return task

    task['notes'] = f"Unknown current node {current_node!r}. Inspect state/graph_state.json before continuing."
    return task


def render_supervisor_context(
    supervisor_task: Dict[str, Any],
    graph_state: Dict[str, Any],
    latest_run: Dict[str, Any],
    diagnosis: Dict[str, Any],
    active_direction: Dict[str, Any],
    round_loop: Dict[str, Any],
) -> str:
    lines = ['# Supervisor context', '']
    lines.append('This file is for the main Codex supervisor. It decides whether to run the next step directly or dispatch a sub-agent.')
    lines.append('')
    lines.append('## Current dispatch')
    lines.append('')
    lines.append(f"- dispatch node: `{supervisor_task.get('dispatch_node', 'node_a')}`")
    lines.append(f"- dispatch mode: `{supervisor_task.get('dispatch_mode', 'direct_script')}`")
    lines.append(f"- graph status: `{supervisor_task.get('graph_status', 'unknown')}`")
    lines.append(f"- round label: `{supervisor_task.get('round_label', 'single-run')}`")
    lines.append(f"- round loop active: `{'yes' if supervisor_task.get('round_loop_active') else 'no'}`")
    lines.append(f"- rounds remaining: `{supervisor_task.get('rounds_remaining', 0)}`")
    lines.append(f"- latest run id: `{latest_run.get('run_id', 'N/A')}`")
    lines.append(f"- latest runtime: `{fmt_runtime(latest_run.get('median_runtime_ms'))}`")
    lines.append(f"- recommended direction: `{diagnosis.get('recommended_direction_id', 'N/A')}`")
    lines.append(f"- active direction: `{active_direction.get('direction_id', 'N/A')}`")
    lines.append('')
    lines.append('## Supervisor protocol')
    lines.append('')
    lines.append('- read `docs/supervisor_protocol.md` first')
    lines.append(f"- node-specific protocol: `{supervisor_task.get('protocol_doc', 'N/A')}`")
    if supervisor_task.get('context_file'):
        lines.append(f"- node context file: `{supervisor_task.get('context_file')}`")
    if supervisor_task.get('prepare_command'):
        lines.append(f"- prepare command: `{supervisor_task.get('prepare_command')}`")
    if supervisor_task.get('selection_command'):
        lines.append(f"- selection command: `{supervisor_task.get('selection_command')}`")
    if supervisor_task.get('finalize_command'):
        lines.append(f"- finalize command: `{supervisor_task.get('finalize_command')}`")
    lines.append(f"- current dispatch requires direct GPU access: `{'yes' if supervisor_task.get('requires_gpu_access') else 'no'}`")
    lines.append('')
    lines.append('## Dispatch rule')
    lines.append('')
    if supervisor_task.get('dispatch_mode') == 'direct_script':
        lines.append('- run the script-first node directly from the main agent')
        lines.append('- do not spawn a sub-agent for node_a')
        lines.append('- after node_a finishes, re-read `state/supervisor_task.json` and continue')
    else:
        lines.append('- main agent stays responsible for graph state, commits, and loop control')
        lines.append('- spawn exactly one sub-agent for the current node')
        lines.append('- after the sub-agent returns, run the finalize command from the main agent')
        lines.append('- then re-read `state/supervisor_task.json` before dispatching the next node')
    lines.append('')
    lines.append('## Multi-round loop')
    lines.append('')
    if round_loop.get('active'):
        lines.append(f"- active loop: `{round_label(round_loop)}` with `{round_loop.get('remaining_rounds', 0)}` rounds remaining")
        lines.append(f"- auto-use recommended: `{'yes' if round_loop.get('auto_use_recommended') else 'no'}`")
        lines.append('- keep looping until `state/round_loop_state.json` reports `remaining_rounds = 0` or a failure pauses the loop')
    else:
        lines.append('- no multi-round loop is active')
        lines.append('- to arm one, run `python scripts/graph.py rounds --count N --auto-use-recommended`')
    lines.append('')
    lines.append('## Notes')
    lines.append('')
    lines.append(f"- `{supervisor_task.get('notes', graph_state.get('notes', 'N/A'))}`")
    return '\n'.join(lines) + '\n'


def refresh_human_state() -> None:
    graph_state = load_graph_state()
    latest_run = load_latest_run()
    latest_ncu = load_latest_ncu_summary()
    diagnosis = load_latest_diagnosis()
    active_direction = load_active_direction()
    benchmark_state = load_benchmark_state()
    round_loop = load_round_loop_state()
    write_text(LATEST_RUN_MD_PATH, render_latest_run_md(latest_run))
    write_text(LATEST_NCU_SUMMARY_MD_PATH, render_latest_ncu_md(latest_ncu))
    write_text(BENCHMARK_BASELINES_MD_PATH, render_benchmark_baselines_md(benchmark_state))
    write_text(ROUNDS_MD_PATH, render_rounds_md(round_loop))
    write_text(PROGRESS_MD_PATH, render_progress_md(graph_state, latest_run, diagnosis, active_direction, benchmark_state, round_loop))
    write_text(CURRENT_FOCUS_MD_PATH, render_current_focus_md(graph_state, latest_run, diagnosis, active_direction, round_loop))
    write_text(HUMAN_REVIEW_MD_PATH, render_human_review_md(graph_state, diagnosis, active_direction, round_loop))


def refresh_supervisor_state() -> None:
    graph_state = load_graph_state()
    latest_run = load_latest_run()
    diagnosis = load_latest_diagnosis()
    active_direction = load_active_direction()
    round_loop = load_round_loop_state()
    supervisor_task = compute_supervisor_task(graph_state, diagnosis, active_direction, round_loop)
    write_json(SUPERVISOR_TASK_PATH, supervisor_task)
    write_text(
        SUPERVISOR_CONTEXT_MD_PATH,
        render_supervisor_context(
            supervisor_task,
            graph_state,
            latest_run,
            diagnosis,
            active_direction,
            round_loop,
        ),
    )


def refresh_node_b_context() -> None:
    write_text(
        NODE_B_CONTEXT_PATH,
        render_node_b_context(
            load_graph_state(),
            load_latest_run(),
            load_latest_ncu_summary(),
            load_latest_diagnosis(),
            load_round_loop_state(),
        ),
    )


def refresh_all_views() -> None:
    refresh_human_state()
    refresh_node_b_context()
    refresh_node_c_context()
    refresh_supervisor_state()


def tracked_dirty_paths() -> List[str]:
    dirty: set[str] = set()
    for args in (
        ['diff', '--name-only'],
        ['diff', '--cached', '--name-only'],
    ):
        output = git_optional_output(args) or ''
        for line in output.splitlines():
            path = line.strip()
            if path:
                dirty.add(path)
    return sorted(dirty)


def refresh_node_c_context() -> None:
    dirty_paths = [path for path in tracked_dirty_paths() if path_is_allowed(path, ALLOWED_NODE_C_PATHS)]
    write_text(
        NODE_C_CONTEXT_PATH,
        render_node_c_context(
            load_graph_state(),
            load_latest_diagnosis(),
            load_active_direction(),
            dirty_paths,
            load_round_loop_state(),
        ),
    )


def start_round_loop(count: int, *, auto_use_recommended: bool) -> Dict[str, Any]:
    latest_run = load_latest_run()
    round_loop = default_round_loop_state()
    round_loop.update(
        {
            'active': True,
            'status': 'running',
            'total_rounds': count,
            'completed_rounds': 0,
            'remaining_rounds': count,
            'next_round_index': 1,
            'current_round_index': None,
            'auto_use_recommended': auto_use_recommended,
            'started_at': now_local_iso(),
            'completed_at': None,
            'last_completed_round': None,
            'accepted_base_run_id': latest_run.get('run_id'),
            'accepted_base_measured_commit': latest_run.get('measured_commit'),
            'accepted_base_runtime_ms': latest_run.get('median_runtime_ms'),
            'notes': (
                f'Started a {count}-round loop. '
                + ('Recommended directions will auto-select.' if auto_use_recommended else 'Direction approval remains manual.')
            ),
        }
    )
    write_json(ROUND_LOOP_STATE_PATH, round_loop)
    return round_loop


def mark_round_started_if_needed(round_loop: Dict[str, Any]) -> Dict[str, Any]:
    if not round_loop.get('active'):
        return round_loop
    if round_loop.get('current_round_index') is None and round_loop.get('remaining_rounds', 0) > 0:
        round_loop['current_round_index'] = round_loop.get('next_round_index', 1)
        round_loop['status'] = 'round_in_progress'
        round_loop['notes'] = f'Executing {round_label(round_loop)}.'
        write_json(ROUND_LOOP_STATE_PATH, round_loop)
    return round_loop


def complete_round(round_loop: Dict[str, Any], round_entry: Dict[str, Any]) -> Dict[str, Any]:
    if not round_loop.get('active'):
        return round_loop
    accepted_runtime = round_loop.get('accepted_base_runtime_ms')
    candidate_runtime = round_entry.get('median_runtime_ms')
    candidate_ok = bool(round_entry.get('correctness_passed'))
    if (
        candidate_ok
        and candidate_runtime is not None
        and (accepted_runtime is None or float(candidate_runtime) < float(accepted_runtime))
    ):
        round_loop['accepted_base_run_id'] = round_entry.get('run_id')
        round_loop['accepted_base_measured_commit'] = round_entry.get('measured_commit')
        round_loop['accepted_base_runtime_ms'] = candidate_runtime
    round_loop['completed_rounds'] = int(round_loop.get('completed_rounds', 0)) + 1
    round_loop['remaining_rounds'] = max(int(round_loop.get('total_rounds', 0)) - int(round_loop.get('completed_rounds', 0)), 0)
    round_loop['next_round_index'] = int(round_loop.get('completed_rounds', 0)) + 1
    round_loop['current_round_index'] = None
    round_loop['last_completed_round'] = round_entry
    append_jsonl(ROUND_HISTORY_PATH, round_entry)
    if round_loop['remaining_rounds'] == 0:
        round_loop['active'] = False
        round_loop['status'] = 'completed'
        round_loop['completed_at'] = now_local_iso()
        round_loop['notes'] = f"Completed {round_loop.get('total_rounds', 0)} planned rounds."
    else:
        round_loop['status'] = 'running'
        round_loop['notes'] = (
            f"Completed round {round_entry.get('round_index')}/{round_entry.get('total_rounds')}. "
            f"Continue with node_b for round {round_loop.get('next_round_index')}/{round_loop.get('total_rounds')}. "
            f"Accepted base: {round_loop.get('accepted_base_run_id') or 'N/A'} at "
            f"{fmt_runtime(round_loop.get('accepted_base_runtime_ms'))}."
        )
    write_json(ROUND_LOOP_STATE_PATH, round_loop)
    return round_loop


def stop_round_loop(message: str) -> Dict[str, Any]:
    round_loop = load_round_loop_state()
    round_loop['active'] = False
    round_loop['status'] = 'stopped'
    round_loop['current_round_index'] = None
    round_loop['completed_at'] = now_local_iso()
    round_loop['notes'] = message
    write_json(ROUND_LOOP_STATE_PATH, round_loop)
    return round_loop


def reset_post_measurement_direction_state(graph_state: Dict[str, Any], latest_run: Dict[str, Any]) -> None:
    diagnosis = default_latest_diagnosis()
    diagnosis['source_run_id'] = latest_run.get('run_id')
    diagnosis['source_run_dir'] = latest_run.get('run_dir')
    diagnosis['source_summary_json'] = latest_run.get('raw_summary_json')
    diagnosis['source_ncu_summary_json'] = repo_rel(LATEST_NCU_SUMMARY_PATH)
    diagnosis['current_kernel_path'] = graph_state.get('current_kernel_path', current_kernel_path())
    diagnosis['notes'] = 'Run node_b to produce exactly three directions from the latest measured run.'
    write_json(LATEST_DIAGNOSIS_PATH, diagnosis)
    write_json(ACTIVE_DIRECTION_PATH, default_active_direction())


def node_a_commit_message(
    latest_run: Dict[str, Any],
    ncu_summary: Dict[str, Any],
    previous_run: Dict[str, Any],
    active_direction: Dict[str, Any],
    round_loop: Dict[str, Any],
    round_entry: Optional[Dict[str, Any]],
) -> str:
    tensor = (ncu_summary.get('headline_metrics') or {}).get('sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active', 'N/A')
    runtime_delta, tflops_delta, verdict = compute_perf_delta(previous_run, latest_run)
    direction_summary = active_direction.get('summary') or {}
    direction_origin = direction_summary.get('idea_origin', 'auto-analysis')
    round_info = round_label(round_loop if round_entry is None else {'current_round_index': round_entry.get('round_index'), 'total_rounds': round_entry.get('total_rounds')})
    if round_entry and not round_loop.get('active'):
        follow_up = 'planned multi-round loop is complete; review results before starting another loop'
    elif round_entry and round_loop.get('active'):
        follow_up = 'multi-round loop continues with node_b'
    else:
        follow_up = 'node_b must now propose exactly three directions from the committed summaries'
    return textwrap.dedent(
        f'''\
        node_a: {round_info} measured {latest_run.get('run_id', 'unknown')} for {latest_run.get('kernel_tag', 'unknown')}

        Why:
        - capture a real measurement for the current custom kernel state
        - advance the workflow from node_a to node_b with committed summaries

        What changed:
        - updated graph state and latest lightweight run summaries
        - updated the latest Nsight Compute headline summary
        - refreshed human-readable progress and focus files
        - implementation idea: {active_direction.get('direction_id', 'N/A')} {direction_summary.get('name', 'N/A')}
        - selection mode: {active_direction.get('selection_mode', 'N/A')}
        - idea origin: {direction_origin}
        - hypothesis: {direction_summary.get('hypothesis', 'N/A')}

        Measurement:
        - run id: {latest_run.get('run_id', 'N/A')}
        - previous run id: {previous_run.get('run_id', 'N/A')}
        - median runtime: {fmt_runtime(latest_run.get('median_runtime_ms'))}
        - runtime delta vs previous measured run: {fmt_delta_ms(runtime_delta)} ({verdict})
        - TFLOP/s: {fmt_tflops(latest_run.get('tflops'))}
        - TFLOP/s delta vs previous measured run: {fmt_delta_tflops(tflops_delta)}
        - correctness: {'PASS' if latest_run.get('correctness_passed') else 'FAIL'}
        - tensor pipe active: {tensor}
        - run dir: {latest_run.get('run_dir', 'N/A')}
        - ncu summary json: {latest_run.get('ncu_summary_json', 'N/A')}
        - ncu rep path: {latest_run.get('ncu_rep_path', 'N/A')}

        Risk / follow-up:
        - {follow_up}
        '''
    )


def node_b_commit_message(diagnosis: Dict[str, Any], latest_run: Dict[str, Any], round_loop: Dict[str, Any]) -> str:
    names = ', '.join(direction.get('name', direction.get('direction_id', 'dir_xx')) for direction in diagnosis.get('directions', []))
    recommended = direction_lookup(diagnosis, diagnosis.get('recommended_direction_id') or '')
    recommended_origin = recommended.get('idea_origin', 'auto-analysis') if recommended else 'auto-analysis'
    return textwrap.dedent(
        f'''\
        node_b: {round_label(round_loop)} rank 3 directions from {latest_run.get('run_id', 'unknown')}

        Why:
        - turn the latest measured run into one concrete implementation choice
        - keep the diagnosis state reproducible and reviewable

        What changed:
        - recorded exactly three optimization directions in state/latest_diagnosis.json
        - updated review and focus state for node_c handoff
        - set the recommended direction to {diagnosis.get('recommended_direction_id', 'N/A')}
        - recommended idea origin: {recommended_origin}

        Measurement:
        - source run id: {latest_run.get('run_id', 'N/A')}
        - source median runtime: {fmt_runtime(latest_run.get('median_runtime_ms'))}
        - source TFLOP/s: {fmt_tflops(latest_run.get('tflops'))}
        - source ncu summary: {repo_rel(LATEST_NCU_SUMMARY_PATH)}
        - source ncu rep path: {load_latest_ncu_summary().get('raw_rep_path', 'N/A')}
        - directions: {names}

        Risk / follow-up:
        - select exactly one direction before node_c starts editing code
        '''
    )


def diagnosis_history_entry(diagnosis: Dict[str, Any], latest_run: Dict[str, Any], round_loop: Dict[str, Any]) -> Dict[str, Any]:
    recommended = direction_lookup(diagnosis, diagnosis.get('recommended_direction_id') or '')
    return {
        'recorded_at': now_local_iso(),
        'round_label': round_label(round_loop),
        'source_run_id': latest_run.get('run_id'),
        'source_run_dir': latest_run.get('run_dir'),
        'source_measured_commit': latest_run.get('measured_commit'),
        'diagnosis_id': diagnosis.get('diagnosis_id'),
        'notes': diagnosis.get('notes'),
        'recommended_direction_id': diagnosis.get('recommended_direction_id'),
        'recommended_idea_origin': recommended.get('idea_origin', 'auto-analysis') if recommended else 'auto-analysis',
        'approved_direction_id': diagnosis.get('approved_direction_id'),
        'current_kernel_path': diagnosis.get('current_kernel_path'),
        'directions': diagnosis.get('directions', []),
    }


def node_c_commit_message(active_direction: Dict[str, Any], direction: Dict[str, Any], round_loop: Dict[str, Any]) -> str:
    direction_origin = direction.get('idea_origin', 'auto-analysis')
    return textwrap.dedent(
        f'''\
        node_c: {round_label(round_loop)} implement {active_direction.get('direction_id', 'dir_xx')} {direction.get('name', 'unnamed')}

        Why:
        - apply one node_b direction without mixing in extra hypotheses
        - get the codebase back to a buildable state before re-measurement

        What changed:
        - updated the implementation surface for the selected direction
        - selection mode: {active_direction.get('selection_mode', 'N/A')}
        - idea origin: {direction_origin}
        - implementation hypothesis: {direction.get('hypothesis', 'N/A')}
        - expected bottleneck: {direction.get('expected_bottleneck', 'N/A')}
        - code locations: {', '.join(direction.get('code_locations', [])) or 'N/A'}
        - refreshed workflow state to hand control back to node_a

        Measurement:
        - build: PASS
        - performance: not claimed here
        - correctness: not claimed here
        - next required node: node_a

        Risk / follow-up:
        - node_a must run before any performance claim is made
        '''
    )


def infra_restore_commit_message(source_commit: str, reason: str) -> str:
    return textwrap.dedent(
        f'''\
        infra: restore implementation surface from {source_commit}

        Why:
        - recover a known measured implementation baseline without erasing later history
        - keep regressed node_c/node_a attempts in git for later summary and comparison

        What changed:
        - restored the allowed implementation surface from measured commit {source_commit}
        - limited the restore to node_c-owned code paths
        - left lightweight state and run history intact

        Risk / follow-up:
        - {reason}
        '''
    )


def node_state_paths_for_commit(extra_paths: Optional[Sequence[Path | str]] = None) -> List[Path | str]:
    paths: List[Path | str] = [
        GRAPH_STATE_PATH,
        SUPERVISOR_TASK_PATH,
        LATEST_RUN_PATH,
        LATEST_RUN_MD_PATH,
        LATEST_NCU_SUMMARY_PATH,
        LATEST_NCU_SUMMARY_MD_PATH,
        LATEST_DIAGNOSIS_PATH,
        ACTIVE_DIRECTION_PATH,
        BENCHMARK_STATE_PATH,
        ROUND_LOOP_STATE_PATH,
        ROUND_HISTORY_PATH,
        DIAGNOSIS_HISTORY_PATH,
        RUN_REGISTRY_PATH,
        ROUNDS_MD_PATH,
        PROGRESS_MD_PATH,
        CURRENT_FOCUS_MD_PATH,
        HUMAN_REVIEW_MD_PATH,
        BENCHMARK_BASELINES_MD_PATH,
        NODE_B_CONTEXT_PATH,
        NODE_C_CONTEXT_PATH,
        SUPERVISOR_CONTEXT_MD_PATH,
    ]
    if extra_paths:
        paths.extend(extra_paths)
    return paths


def existing_node_c_support_paths() -> List[Path]:
    extra_paths: List[Path] = [REPO_ROOT / 'scripts' / 'graph.py']
    if SWEEP_FIXED_MAIN_TILES_PATH.exists():
        extra_paths.append(SWEEP_FIXED_MAIN_TILES_PATH)
    extra_paths.extend(sorted(path for path in STATE_DIR.glob('autotune_*_main_tiles.*') if path.is_file()))
    return extra_paths


def update_failure_state(node_name: str, message: str) -> None:
    graph_state = load_graph_state()
    graph_state['current_node'] = node_name
    graph_state['status'] = f'{node_name}_failed'
    graph_state['notes'] = message
    write_json(GRAPH_STATE_PATH, graph_state)
    round_loop = load_round_loop_state()
    if round_loop.get('active'):
        round_loop['status'] = f'paused_on_{node_name}_failure'
        round_loop['notes'] = f'Paused {round_label(round_loop)} because {node_name} failed: {message}'
        write_json(ROUND_LOOP_STATE_PATH, round_loop)
    refresh_all_views()


def run_restore_implementation(args: argparse.Namespace) -> int:
    ensure_machine_state()
    source_commit = args.source_commit.strip()
    if not source_commit:
        raise RuntimeError('restore-implementation requires --source-commit <sha>')

    tracked_non_state = [
        path for path in tracked_dirty_paths()
        if not path.startswith('state/')
    ]
    unrelated_dirty = [
        path for path in tracked_non_state
        if not path_is_allowed(path, ALLOWED_NODE_C_PATHS)
    ]
    if unrelated_dirty:
        raise RuntimeError(
            'refusing restore because unrelated tracked changes are present: '
            + ', '.join(unrelated_dirty)
        )

    changed_paths = restore_paths_from_commit(source_commit, ALLOWED_NODE_C_PATHS)
    refresh_node_c_context()

    if not changed_paths:
        print_step(f'implementation surface already matches {source_commit}')
        return 0

    if not args.skip_commit:
        commit_paths(
            changed_paths,
            infra_restore_commit_message(
                source_commit,
                args.reason or 're-measure or continue the next round from the restored baseline',
            ),
        )

    print_step(
        f'restored {len(changed_paths)} implementation path(s) from {source_commit}'
    )
    return 0


def run_node_a(args: argparse.Namespace) -> int:
    ensure_node_a_can_access_gpu()
    ensure_machine_state()
    graph_state = load_graph_state()
    previous_run = load_latest_run()
    active_direction_before = load_active_direction()
    round_loop = load_round_loop_state()
    graph_state['current_kernel_path'] = graph_state.get('current_kernel_path') or current_kernel_path()
    write_json(GRAPH_STATE_PATH, graph_state)

    runner_path = REPO_ROOT / args.runner
    dataset_dir = REPO_ROOT / 'artifacts' / 'datasets' / 'fixed_bf16_gemm_v1'
    if not dataset_dir.exists():
        update_failure_state('node_a', 'dataset not found; run python scripts/generate_fixed_bf16_dataset.py first')
        raise FileNotFoundError(f'dataset not found: {repo_rel(dataset_dir)}')

    if args.dry_run:
        print_step('node_a dry run')
        print(f'runner: {repo_rel(runner_path)}')
        print(f'kernel tag: {args.kernel_tag or default_kernel_tag(graph_state["current_kernel_path"])}')
        return 0

    if not maybe_run_build(runner_path, force=args.force_build, log_path=NODE_A_BUILD_LOG_PATH):
        update_failure_state('node_a', f'build failed; inspect {repo_rel(NODE_A_BUILD_LOG_PATH)}')
        raise RuntimeError(f'node_a build failed; see {repo_rel(NODE_A_BUILD_LOG_PATH)}')

    measured_commit = head_commit()
    cmd = [
        sys.executable,
        str(REPO_ROOT / 'scripts' / 'eval_kernel.py'),
        '--runner',
        str(runner_path),
        '--kernel-tag',
        args.kernel_tag or default_kernel_tag(graph_state['current_kernel_path']),
        '--config',
        str(REPO_ROOT / 'configs' / 'fixed_bf16_gemm_v1.json'),
        '--dataset-root',
        str(REPO_ROOT / 'artifacts' / 'datasets'),
        '--runs-root',
        str(RUNS_DIR),
        '--ncu-metrics-file',
        str(REPO_ROOT / 'configs' / 'ncu_metrics_core.txt'),
    ]
    if args.skip_ncu:
        cmd.append('--skip-ncu')
    if args.warmup is not None:
        cmd.extend(['--warmup', str(args.warmup)])
    if args.iters is not None:
        cmd.extend(['--iters', str(args.iters)])

    proc = run_command(cmd, capture=True)
    if proc.returncode != 0:
        update_failure_state('node_a', 'evaluation failed; inspect the latest run logs under runs/')
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or 'node_a evaluation failed')

    run_dir = parse_run_dir_from_stdout(proc.stdout)
    benchmark_state = load_benchmark_state()
    latest_run, latest_ncu, is_new_best = summarize_run(run_dir, measured_commit, benchmark_state)
    runtime_delta, tflops_delta, verdict = compute_perf_delta(previous_run, latest_run)
    latest_run['previous_run_id'] = previous_run.get('run_id')
    latest_run['previous_median_runtime_ms'] = previous_run.get('median_runtime_ms')
    latest_run['runtime_delta_ms'] = runtime_delta
    latest_run['tflops_delta'] = tflops_delta
    latest_run['perf_verdict'] = verdict
    latest_run['implemented_direction_id'] = active_direction_before.get('direction_id')
    latest_run['implemented_direction_name'] = (active_direction_before.get('summary') or {}).get('name')
    latest_run['implemented_selection_mode'] = active_direction_before.get('selection_mode')
    latest_run['implemented_idea_origin'] = (active_direction_before.get('summary') or {}).get('idea_origin', 'auto-analysis')
    latest_run['round_label'] = round_label(round_loop) if active_direction_before.get('status') == 'implemented_pending_measurement' else 'single-run'
    if is_new_best:
        update_best_custom(benchmark_state, latest_run)
        graph_state['plateau_counter'] = 0
    else:
        graph_state['plateau_counter'] = int(graph_state.get('plateau_counter', 0)) + 1
    write_json(BENCHMARK_STATE_PATH, benchmark_state)
    write_json(LATEST_RUN_PATH, latest_run)
    write_json(LATEST_NCU_SUMMARY_PATH, latest_ncu)
    append_jsonl(
        RUN_REGISTRY_PATH,
        {
            'recorded_at': now_local_iso(),
            'run_id': latest_run.get('run_id'),
            'run_dir': latest_run.get('run_dir'),
            'kernel_tag': latest_run.get('kernel_tag'),
            'median_runtime_ms': latest_run.get('median_runtime_ms'),
            'tflops': latest_run.get('tflops'),
            'runtime_delta_ms': latest_run.get('runtime_delta_ms'),
            'tflops_delta': latest_run.get('tflops_delta'),
            'perf_verdict': latest_run.get('perf_verdict'),
            'implemented_direction_id': latest_run.get('implemented_direction_id'),
            'implemented_direction_name': latest_run.get('implemented_direction_name'),
            'implemented_selection_mode': latest_run.get('implemented_selection_mode'),
            'implemented_idea_origin': latest_run.get('implemented_idea_origin'),
            'round_label': latest_run.get('round_label'),
            'correctness_passed': latest_run.get('correctness_passed'),
            'measured_commit': latest_run.get('measured_commit'),
        },
    )

    round_entry = None
    if round_loop.get('active') and active_direction_before.get('status') == 'implemented_pending_measurement':
        round_entry = {
            'recorded_at': now_local_iso(),
            'round_index': active_round_index(round_loop),
            'total_rounds': round_loop.get('total_rounds'),
            'direction_id': active_direction_before.get('direction_id'),
            'direction_name': (active_direction_before.get('summary') or {}).get('name'),
            'selection_mode': active_direction_before.get('selection_mode'),
            'idea_origin': (active_direction_before.get('summary') or {}).get('idea_origin', 'auto-analysis'),
            'hypothesis': (active_direction_before.get('summary') or {}).get('hypothesis'),
            'previous_run_id': previous_run.get('run_id'),
            'run_id': latest_run.get('run_id'),
            'run_dir': latest_run.get('run_dir'),
            'median_runtime_ms': latest_run.get('median_runtime_ms'),
            'runtime_delta_ms': runtime_delta,
            'tflops': latest_run.get('tflops'),
            'tflops_delta': tflops_delta,
            'perf_verdict': verdict,
            'correctness_passed': latest_run.get('correctness_passed'),
            'measured_commit': latest_run.get('measured_commit'),
            'ncu_summary_json': latest_run.get('ncu_summary_json'),
            'ncu_rep_path': latest_run.get('ncu_rep_path'),
        }
        round_loop = complete_round(round_loop, round_entry)

    graph_state['current_node'] = 'node_b'
    graph_state['previous_node'] = 'node_a'
    graph_state['status'] = 'ready_for_node_b'
    graph_state['latest_run_dir'] = latest_run.get('run_dir')
    graph_state['latest_summary_json'] = repo_rel(LATEST_RUN_PATH)
    graph_state['latest_ncu_summary_json'] = repo_rel(LATEST_NCU_SUMMARY_PATH)
    graph_state['latest_commit'] = measured_commit
    graph_state['recommended_direction_id'] = None
    graph_state['approved_direction_id'] = None
    if round_entry and round_loop.get('active'):
        graph_state['notes'] = (
            f"Node A completed round {round_entry.get('round_index')}/{round_entry.get('total_rounds')}. "
            f"Run node_b to continue round {round_loop.get('next_round_index')}/{round_loop.get('total_rounds')}."
        )
    elif round_entry and not round_loop.get('active'):
        graph_state['notes'] = 'Node A completed the final planned round. Review the results before starting another loop.'
    else:
        graph_state['notes'] = 'Node A completed. Run node_b to produce exactly three directions from the latest measured summaries.'
    write_json(GRAPH_STATE_PATH, graph_state)
    reset_post_measurement_direction_state(graph_state, latest_run)
    refresh_all_views()

    if not args.skip_commit:
        commit_paths(
            node_state_paths_for_commit(),
            node_a_commit_message(latest_run, latest_ncu, previous_run, active_direction_before, round_loop, round_entry),
        )

    print_step(f'node_a completed; next node is node_b ({latest_run.get("run_id")})')
    return 0


def diagnosis_template(latest_run: Dict[str, Any], graph_state: Dict[str, Any]) -> Dict[str, Any]:
    diagnosis = default_latest_diagnosis()
    diagnosis['diagnosis_id'] = f'diagnosis_{timestamp_tag()}'
    diagnosis['status'] = 'awaiting_codex'
    diagnosis['created_at'] = now_local_iso()
    diagnosis['source_run_id'] = latest_run.get('run_id')
    diagnosis['source_run_dir'] = latest_run.get('run_dir')
    diagnosis['source_summary_json'] = latest_run.get('raw_summary_json')
    diagnosis['source_ncu_summary_json'] = repo_rel(LATEST_NCU_SUMMARY_PATH)
    diagnosis['current_kernel_path'] = graph_state.get('current_kernel_path', current_kernel_path())
    diagnosis['directions'] = [
        {
            'direction_id': 'dir_01',
            'rank': 1,
            'name': '',
            'hypothesis': '',
            'expected_bottleneck': '',
            'code_locations': [],
            'risk': '',
            'metrics_to_recheck': [],
            'stop_condition': '',
        },
        {
            'direction_id': 'dir_02',
            'rank': 2,
            'name': '',
            'hypothesis': '',
            'expected_bottleneck': '',
            'code_locations': [],
            'risk': '',
            'metrics_to_recheck': [],
            'stop_condition': '',
        },
        {
            'direction_id': 'dir_03',
            'rank': 3,
            'name': '',
            'hypothesis': '',
            'expected_bottleneck': '',
            'code_locations': [],
            'risk': '',
            'metrics_to_recheck': [],
            'stop_condition': '',
        },
    ]
    return diagnosis


def validate_diagnosis(diagnosis: Dict[str, Any]) -> None:
    directions = diagnosis.get('directions', [])
    if len(directions) != 3:
        raise RuntimeError('node_b requires exactly 3 directions')
    seen_ids = set()
    for direction in directions:
        direction_id = direction.get('direction_id')
        if not direction_id:
            raise RuntimeError('every direction needs a direction_id')
        if direction_id in seen_ids:
            raise RuntimeError(f'duplicate direction id: {direction_id}')
        seen_ids.add(direction_id)
        for key in ('name', 'hypothesis', 'expected_bottleneck', 'risk', 'stop_condition'):
            value = direction.get(key)
            if not isinstance(value, str) or not value.strip():
                raise RuntimeError(f'{direction_id} is missing non-empty field: {key}')
        code_locations = direction.get('code_locations')
        if not isinstance(code_locations, list) or not code_locations or not all(isinstance(item, str) and item.strip() for item in code_locations):
            raise RuntimeError(f'{direction_id} needs a non-empty code_locations list')
        metrics = direction.get('metrics_to_recheck')
        if not isinstance(metrics, list) or not metrics or not all(isinstance(item, str) and item.strip() for item in metrics):
            raise RuntimeError(f'{direction_id} needs a non-empty metrics_to_recheck list')

    recommended = diagnosis.get('recommended_direction_id')
    if recommended not in seen_ids:
        raise RuntimeError('recommended_direction_id must reference one of the three directions')


def run_node_b(args: argparse.Namespace) -> int:
    ensure_machine_state()
    latest_run = load_latest_run()
    if not latest_run.get('run_id'):
        raise RuntimeError('node_b requires a measured run first; run node_a')

    graph_state = load_graph_state()
    round_loop = load_round_loop_state()
    if args.finalize:
        diagnosis = load_json_file(REPO_ROOT / args.diagnosis_file)
        validate_diagnosis(diagnosis)
        diagnosis['status'] = 'completed'
        diagnosis['created_at'] = diagnosis.get('created_at') or now_local_iso()
        diagnosis['source_run_id'] = diagnosis.get('source_run_id') or latest_run.get('run_id')
        diagnosis['source_run_dir'] = diagnosis.get('source_run_dir') or latest_run.get('run_dir')
        diagnosis['source_summary_json'] = diagnosis.get('source_summary_json') or latest_run.get('raw_summary_json')
        diagnosis['source_ncu_summary_json'] = diagnosis.get('source_ncu_summary_json') or repo_rel(LATEST_NCU_SUMMARY_PATH)
        diagnosis['current_kernel_path'] = diagnosis.get('current_kernel_path') or graph_state.get('current_kernel_path', current_kernel_path())
        write_json(LATEST_DIAGNOSIS_PATH, diagnosis)

        graph_state['current_node'] = 'node_c'
        graph_state['previous_node'] = 'node_b'
        graph_state['status'] = 'awaiting_direction_selection_for_node_c'
        graph_state['recommended_direction_id'] = diagnosis.get('recommended_direction_id')
        graph_state['approved_direction_id'] = diagnosis.get('approved_direction_id')
        graph_state['notes'] = 'Node B completed. Approve a direction or explicitly use the recommended direction before node_c.'
        write_json(GRAPH_STATE_PATH, graph_state)
        write_json(ACTIVE_DIRECTION_PATH, default_active_direction())
        append_jsonl(
            DIAGNOSIS_HISTORY_PATH,
            diagnosis_history_entry(diagnosis, latest_run, round_loop),
        )
        if round_loop.get('active') and round_loop.get('auto_use_recommended'):
            select_direction(diagnosis.get('recommended_direction_id'), 'recommended')
            round_loop = load_round_loop_state()
        refresh_all_views()
        if not args.skip_commit:
            commit_paths(node_state_paths_for_commit(), node_b_commit_message(diagnosis, latest_run, round_loop))
        if round_loop.get('active') and round_loop.get('auto_use_recommended'):
            print_step('node_b finalized; auto-selected the recommended direction for node_c')
        else:
            print_step('node_b finalized; next node is node_c')
        return 0

    diagnosis = load_latest_diagnosis()
    needs_refresh = args.refresh_template or diagnosis.get('source_run_id') != latest_run.get('run_id') or diagnosis.get('status') in (None, 'pending_generation')
    if needs_refresh:
        diagnosis = diagnosis_template(latest_run, graph_state)
        write_json(LATEST_DIAGNOSIS_PATH, diagnosis)

    graph_state['current_node'] = 'node_b'
    graph_state['status'] = 'node_b_context_ready'
    if round_loop.get('active'):
        graph_state['notes'] = f"Fill state/latest_diagnosis.json with exactly three directions for {round_label(round_loop)}, then run node_b --finalize."
    else:
        graph_state['notes'] = 'Fill state/latest_diagnosis.json with exactly three directions, then run node_b --finalize.'
    write_json(GRAPH_STATE_PATH, graph_state)
    refresh_all_views()
    print_step(f'node_b context prepared at {repo_rel(NODE_B_CONTEXT_PATH)}')
    return 0


def select_direction(direction_id: str, selection_mode: str) -> int:
    ensure_machine_state()
    if not direction_id:
        raise RuntimeError('no direction is available yet; finalize node_b first')
    diagnosis = load_latest_diagnosis()
    if diagnosis.get('status') != 'completed':
        raise RuntimeError('node_b must be finalized before selecting a direction')
    direction = direction_lookup(diagnosis, direction_id)
    if direction is None:
        raise RuntimeError(f'unknown direction id: {direction_id}')

    active = {
        'direction_id': direction_id,
        'name': direction.get('name'),
        'selection_mode': selection_mode,
        'selected_at': now_local_iso(),
        'source_diagnosis_id': diagnosis.get('diagnosis_id'),
        'status': 'ready_for_implementation',
        'summary': direction,
        'notes': 'Node C may now implement this one direction.',
    }
    write_json(ACTIVE_DIRECTION_PATH, active)

    if selection_mode in ('approved', 'human_idea'):
        diagnosis['approved_direction_id'] = direction_id
    write_json(LATEST_DIAGNOSIS_PATH, diagnosis)

    round_loop = mark_round_started_if_needed(load_round_loop_state())
    graph_state = load_graph_state()
    graph_state['current_node'] = 'node_c'
    graph_state['previous_node'] = 'node_b'
    graph_state['status'] = 'ready_for_node_c'
    graph_state['recommended_direction_id'] = diagnosis.get('recommended_direction_id')
    graph_state['approved_direction_id'] = diagnosis.get('approved_direction_id')
    if round_loop.get('active'):
        graph_state['notes'] = f'Node C is ready to implement {direction_id} via {selection_mode} selection for {round_label(round_loop)}.'
    else:
        graph_state['notes'] = f'Node C is ready to implement {direction_id} via {selection_mode} selection.'
    write_json(GRAPH_STATE_PATH, graph_state)
    refresh_all_views()
    print_step(f'selected {direction_id} for node_c using mode={selection_mode}')
    return 0


def run_node_c(args: argparse.Namespace) -> int:
    ensure_machine_state()
    graph_state = load_graph_state()
    diagnosis = load_latest_diagnosis()
    active_direction = load_active_direction()
    round_loop = load_round_loop_state()
    if not active_direction.get('direction_id'):
        raise RuntimeError('node_c requires an active direction; use approve or use-recommended-direction first')

    direction = direction_lookup(diagnosis, active_direction.get('direction_id'))
    if direction is None:
        raise RuntimeError('active direction is not present in state/latest_diagnosis.json')

    if not args.finalize:
        graph_state['current_node'] = 'node_c'
        graph_state['status'] = 'node_c_context_ready'
        if round_loop.get('active'):
            graph_state['notes'] = f'Implement the selected direction for {round_label(round_loop)}, then run node_c --finalize.'
        else:
            graph_state['notes'] = 'Implement the selected direction, then run node_c --finalize.'
        write_json(GRAPH_STATE_PATH, graph_state)
        refresh_all_views()
        print_step(f'node_c context prepared at {repo_rel(NODE_C_CONTEXT_PATH)}')
        return 0

    runner_path = REPO_ROOT / 'build' / 'custom_runner'
    if args.dry_run:
        print_step('node_c finalize dry run')
        print(f'active direction: {active_direction.get("direction_id")}')
        print(f'build log path: {repo_rel(NODE_C_BUILD_LOG_PATH)}')
        return 0

    build_ok = maybe_run_build(runner_path, force=args.force_build, log_path=NODE_C_BUILD_LOG_PATH)
    if not build_ok:
        graph_state['current_node'] = 'node_c'
        graph_state['previous_node'] = 'node_b'
        graph_state['status'] = 'node_c_build_failed'
        graph_state['notes'] = f'Build failed for {active_direction.get("direction_id")}; inspect {repo_rel(NODE_C_BUILD_LOG_PATH)}'
        active_direction['status'] = 'build_failed'
        active_direction['notes'] = f'Build failed; inspect {repo_rel(NODE_C_BUILD_LOG_PATH)}'
        write_json(GRAPH_STATE_PATH, graph_state)
        write_json(ACTIVE_DIRECTION_PATH, active_direction)
        if round_loop.get('active'):
            round_loop['status'] = 'paused_on_build_failure'
            round_loop['notes'] = f'Paused {round_label(round_loop)} because node_c failed to build.'
            write_json(ROUND_LOOP_STATE_PATH, round_loop)
        refresh_all_views()
        raise RuntimeError(f'node_c build failed; see {repo_rel(NODE_C_BUILD_LOG_PATH)}')

    active_direction['status'] = 'implemented_pending_measurement'
    active_direction['notes'] = 'Build passed. Node A must measure this implementation next.'
    write_json(ACTIVE_DIRECTION_PATH, active_direction)
    if round_loop.get('active'):
        round_loop['status'] = 'awaiting_measurement'
        round_loop['notes'] = f'Build passed for {round_label(round_loop)}. Node A will measure the result next.'
        write_json(ROUND_LOOP_STATE_PATH, round_loop)
    graph_state['current_node'] = 'node_a'
    graph_state['previous_node'] = 'node_c'
    graph_state['status'] = 'ready_for_node_a'
    if round_loop.get('active'):
        graph_state['notes'] = f'Node C build succeeded for {round_label(round_loop)}. Node A will now measure the new code path.'
    else:
        graph_state['notes'] = 'Node C build succeeded. Node A will now measure the new code path.'
    write_json(GRAPH_STATE_PATH, graph_state)
    refresh_all_views()

    commit_list = node_state_paths_for_commit(
        [
            REPO_ROOT / graph_state.get('current_kernel_path', current_kernel_path()),
            REPO_ROOT / 'src' / 'runner' / 'main.cpp',
            REPO_ROOT / 'src' / 'kernels',
            REPO_ROOT / 'include',
            REPO_ROOT / 'CMakeLists.txt',
            *existing_node_c_support_paths(),
        ]
    )
    if not args.skip_commit:
        commit_paths(commit_list, node_c_commit_message(active_direction, direction, round_loop))

    if args.no_auto_node_a:
        print_step('node_c finalized without auto-running node_a')
        return 0

    auto_args = argparse.Namespace(
        runner='build/custom_runner',
        kernel_tag=None,
        skip_ncu=False,
        warmup=None,
        iters=None,
        force_build=False,
        skip_commit=False,
        dry_run=False,
    )
    return run_node_a(auto_args)


def run_status(_: argparse.Namespace) -> int:
    ensure_machine_state()
    refresh_all_views()
    graph_state = load_graph_state()
    latest_run = load_latest_run()
    diagnosis = load_latest_diagnosis()
    active_direction = load_active_direction()
    benchmark_state = load_benchmark_state()
    round_loop = load_round_loop_state()
    supervisor_task = load_supervisor_task()
    absolute_gap, runtime_ratio = compute_gap(benchmark_state)
    print(f"current_node={graph_state.get('current_node')}")
    print(f"previous_node={graph_state.get('previous_node')}")
    print(f"status={graph_state.get('status')}")
    print(f"dispatch_mode={supervisor_task.get('dispatch_mode')}")
    print(f"dispatch_prepare_command={supervisor_task.get('prepare_command')}")
    print(f"dispatch_finalize_command={supervisor_task.get('finalize_command')}")
    print(f"latest_run_id={latest_run.get('run_id')}")
    print(f"latest_run_dir={latest_run.get('run_dir')}")
    print(f"latest_runtime_ms={latest_run.get('median_runtime_ms')}")
    print(f"recommended_direction_id={diagnosis.get('recommended_direction_id')}")
    print(f"approved_direction_id={diagnosis.get('approved_direction_id')}")
    print(f"active_direction_id={active_direction.get('direction_id')}")
    print(f"round_loop_active={round_loop.get('active')}")
    print(f"round_loop_label={round_label(round_loop)}")
    print(f"rounds_remaining={round_loop.get('remaining_rounds')}")
    print(f"round_loop_status={round_loop.get('status')}")
    print(f"cutlass_gap_ms={absolute_gap}")
    print(f"cutlass_gap_ratio={runtime_ratio}")
    return 0


def run_supervisor(_: argparse.Namespace) -> int:
    ensure_machine_state()
    refresh_all_views()
    supervisor_task = load_supervisor_task()
    print(f"dispatch_node={supervisor_task.get('dispatch_node')}")
    print(f"dispatch_mode={supervisor_task.get('dispatch_mode')}")
    print(f"graph_status={supervisor_task.get('graph_status')}")
    print(f"prepare_command={supervisor_task.get('prepare_command')}")
    print(f"selection_command={supervisor_task.get('selection_command')}")
    print(f"finalize_command={supervisor_task.get('finalize_command')}")
    print(f"protocol_doc={supervisor_task.get('protocol_doc')}")
    print(f"context_file={supervisor_task.get('context_file')}")
    print(f"requires_gpu_access={supervisor_task.get('requires_gpu_access')}")
    print(f"round_label={supervisor_task.get('round_label')}")
    print(f"round_loop_active={supervisor_task.get('round_loop_active')}")
    print(f"rounds_remaining={supervisor_task.get('rounds_remaining')}")
    print(f"notes={supervisor_task.get('notes')}")
    return 0


def run_rounds(args: argparse.Namespace) -> int:
    ensure_machine_state()
    if args.status:
        refresh_all_views()
        round_loop = load_round_loop_state()
        print(f"active={round_loop.get('active')}")
        print(f"status={round_loop.get('status')}")
        print(f"total_rounds={round_loop.get('total_rounds')}")
        print(f"completed_rounds={round_loop.get('completed_rounds')}")
        print(f"remaining_rounds={round_loop.get('remaining_rounds')}")
        print(f"round_label={round_label(round_loop)}")
        print(f"auto_use_recommended={round_loop.get('auto_use_recommended')}")
        print(f"notes={round_loop.get('notes')}")
        return 0

    if args.stop:
        stop_round_loop('Stopped by user request.')
        graph_state = load_graph_state()
        graph_state['notes'] = 'Round loop stopped by user request.'
        write_json(GRAPH_STATE_PATH, graph_state)
        refresh_all_views()
        print_step('stopped the active round loop')
        return 0

    if args.clear:
        write_json(ROUND_LOOP_STATE_PATH, default_round_loop_state())
        graph_state = load_graph_state()
        graph_state['notes'] = 'No multi-round loop is active.'
        write_json(GRAPH_STATE_PATH, graph_state)
        refresh_all_views()
        print_step('cleared the round loop state back to idle')
        return 0

    if args.count is None or args.count <= 0:
        raise RuntimeError('rounds requires --count N, --status, --stop, or --clear')

    current = load_round_loop_state()
    if current.get('active') and not args.restart:
        raise RuntimeError('a round loop is already active; use --restart to replace it or --stop to end it')

    start_round_loop(args.count, auto_use_recommended=args.auto_use_recommended)
    graph_state = load_graph_state()
    graph_state['notes'] = (
        f"Multi-round loop armed for {args.count} rounds. Continue with {graph_state.get('current_node', 'node_a')}."
    )
    write_json(GRAPH_STATE_PATH, graph_state)
    refresh_all_views()
    print_step(
        f"started a {args.count}-round loop"
        + (' with auto-use-recommended enabled' if args.auto_use_recommended else '')
    )
    return 0


def run_cycle(args: argparse.Namespace) -> int:
    current_node = load_graph_state().get('current_node')
    round_loop = load_round_loop_state()
    if current_node == 'node_a':
        return run_node_a(args)
    if current_node == 'node_b':
        return run_node_b(argparse.Namespace(finalize=False, refresh_template=False, diagnosis_file=LATEST_DIAGNOSIS_PATH, skip_commit=False))
    if current_node == 'node_c':
        active_direction = load_active_direction()
        if not active_direction.get('direction_id') and round_loop.get('active') and round_loop.get('auto_use_recommended'):
            diagnosis = load_latest_diagnosis()
            recommended = diagnosis.get('recommended_direction_id')
            if recommended:
                select_direction(recommended, 'recommended')
        return run_node_c(argparse.Namespace(finalize=False, force_build=False, skip_commit=False, no_auto_node_a=False, dry_run=False))
    raise RuntimeError(f'unknown current node: {current_node}')


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Script-first workflow entrypoint for node_a/node_b/node_c')
    subparsers = parser.add_subparsers(dest='command', required=True)

    supervisor = subparsers.add_parser('supervisor', help='Refresh and print the current main-agent dispatch task')
    supervisor.set_defaults(func=run_supervisor)

    node_a = subparsers.add_parser('node_a', help='Run the script-first evaluation node')
    node_a.add_argument('--runner', default='build/custom_runner')
    node_a.add_argument('--kernel-tag', default=None)
    node_a.add_argument('--skip-ncu', action='store_true')
    node_a.add_argument('--warmup', type=int, default=None)
    node_a.add_argument('--iters', type=int, default=None)
    node_a.add_argument('--force-build', action='store_true')
    node_a.add_argument('--skip-commit', action='store_true')
    node_a.add_argument('--dry-run', action='store_true')
    node_a.set_defaults(func=run_node_a)

    node_b = subparsers.add_parser('node_b', help='Prepare or finalize the diagnosis node')
    node_b.add_argument('--finalize', action='store_true')
    node_b.add_argument('--refresh-template', action='store_true')
    node_b.add_argument('--diagnosis-file', type=Path, default=LATEST_DIAGNOSIS_PATH)
    node_b.add_argument('--skip-commit', action='store_true')
    node_b.set_defaults(func=run_node_b)

    node_c = subparsers.add_parser('node_c', help='Prepare or finalize the implementation node')
    node_c.add_argument('--finalize', action='store_true')
    node_c.add_argument('--force-build', action='store_true')
    node_c.add_argument('--skip-commit', action='store_true')
    node_c.add_argument('--no-auto-node-a', action='store_true')
    node_c.add_argument('--dry-run', action='store_true')
    node_c.set_defaults(func=run_node_c)

    cycle = subparsers.add_parser('cycle', help='Run the current actionable node or prepare the next agent handoff')
    cycle.add_argument('--runner', default='build/custom_runner')
    cycle.add_argument('--kernel-tag', default=None)
    cycle.add_argument('--skip-ncu', action='store_true')
    cycle.add_argument('--warmup', type=int, default=None)
    cycle.add_argument('--iters', type=int, default=None)
    cycle.add_argument('--force-build', action='store_true')
    cycle.add_argument('--skip-commit', action='store_true')
    cycle.add_argument('--dry-run', action='store_true')
    cycle.set_defaults(func=run_cycle)

    restore = subparsers.add_parser(
        'restore-implementation',
        help='Restore the node_c-owned implementation surface from a measured commit while preserving later history',
    )
    restore.add_argument('--source-commit', required=True)
    restore.add_argument('--reason', default=None)
    restore.add_argument('--skip-commit', action='store_true')
    restore.set_defaults(func=run_restore_implementation)

    status = subparsers.add_parser('status', help='Print the current graph state')
    status.set_defaults(func=run_status)

    rounds = subparsers.add_parser('rounds', help='Manage a multi-round node_b -> node_c -> node_a loop budget')
    rounds.add_argument('--count', type=int, default=None)
    rounds.add_argument('--auto-use-recommended', action='store_true')
    rounds.add_argument('--restart', action='store_true')
    rounds.add_argument('--status', action='store_true')
    rounds.add_argument('--stop', action='store_true')
    rounds.add_argument('--clear', action='store_true')
    rounds.set_defaults(func=run_rounds)

    approve = subparsers.add_parser('approve', help='Select one explicit node_b direction for node_c')
    approve.add_argument('--direction', required=True)
    approve.set_defaults(func=lambda args: select_direction(args.direction, 'approved'))

    human_idea = subparsers.add_parser('use-human-direction', help='Select one node_b direction for node_c and record it as a human idea')
    human_idea.add_argument('--direction', required=True)
    human_idea.set_defaults(func=lambda args: select_direction(args.direction, 'human_idea'))

    use_recommended = subparsers.add_parser('use-recommended-direction', help='Select the rank-1 recommended direction for node_c')
    use_recommended.set_defaults(
        func=lambda args: select_direction(load_latest_diagnosis().get('recommended_direction_id'), 'recommended')
    )
    return parser


def main() -> int:
    ensure_machine_state()
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except Exception as exc:  # noqa: BLE001
        print_step(f'error: {exc}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
