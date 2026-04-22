#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import shlex
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

import eval_kernel
import ncu_analysis
from search_policy import (
    classify_transition,
    fallback_search_score_v1,
    make_action_fingerprint,
    normalize_risk_text_to_level,
)
from state_lib import (
    ACTIVE_DIRECTION_PATH,
    BENCHMARK_STATE_PATH,
    DIAGNOSIS_HISTORY_PATH,
    DOCS_DIR,
    FAMILY_LEDGER_PATH,
    GRAPH_STATE_PATH,
    LATEST_DIAGNOSIS_PATH,
    LATEST_ATTEMPT_PATH,
    LATEST_NCU_SUMMARY_PATH,
    LATEST_RUN_PATH,
    REPO_ROOT,
    ROUND_HISTORY_PATH,
    ROUND_LOOP_STATE_PATH,
    RUN_REGISTRY_PATH,
    RUNS_DIR,
    SEARCH_CLOSED_PATH,
    SEARCH_CANDIDATES_PATH,
    SEARCH_FRONTIER_PATH,
    SEARCH_STATE_PATH,
    STATE_DIR,
    SUPERVISOR_TASK_PATH,
    append_jsonl,
    current_kernel_path,
    default_active_direction,
    default_family_ledger,
    default_graph_state,
    default_latest_attempt,
    default_latest_ncu_summary,
    default_latest_diagnosis,
    default_latest_run,
    default_round_loop_state,
    default_search_candidates,
    default_search_frontier,
    default_search_state,
    direction_lookup,
    ensure_machine_state,
    load_active_direction,
    load_benchmark_state,
    load_family_ledger,
    load_graph_state,
    load_latest_diagnosis,
    load_latest_attempt,
    load_latest_ncu_summary,
    load_latest_run,
    load_round_loop_state,
    load_run_registry,
    load_search_candidates,
    load_search_frontier,
    load_search_state,
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
HUMAN_GUIDANCE_MD_PATH = STATE_DIR / 'human_guidance.md'
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

RESTORE_IMPLEMENTATION_PATHS = [
    REPO_ROOT / 'src' / 'kernels',
    REPO_ROOT / 'src' / 'runner' / 'main.cpp',
    REPO_ROOT / 'include',
    REPO_ROOT / 'CMakeLists.txt',
]

REBOOTSTRAP_IMPLEMENTATION_PATHS = [
    REPO_ROOT / 'src' / 'kernels',
    REPO_ROOT / 'src' / 'runner' / 'main.cpp',
    REPO_ROOT / 'include',
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


def context_compression_interval() -> int:
    return 5


def checkpoint_round(round_loop: Dict[str, Any], interval: int) -> Optional[int]:
    completed = int(round_loop.get('completed_rounds', 0) or 0)
    if completed < interval:
        return None
    return completed - (completed % interval)


def next_checkpoint_round(round_loop: Dict[str, Any], interval: int) -> Optional[int]:
    if not round_loop.get('active'):
        return None
    total = int(round_loop.get('total_rounds', 0) or 0)
    if total <= 0:
        return None
    completed = int(round_loop.get('completed_rounds', 0) or 0)
    if completed > 0 and completed % interval == 0:
        checkpoint = completed + interval
    else:
        checkpoint = ((completed // interval) + 1) * interval
    if checkpoint > total:
        return None
    return checkpoint


def latest_context_checkpoint_round(round_loop: Dict[str, Any]) -> Optional[int]:
    return checkpoint_round(round_loop, context_compression_interval())


def next_context_checkpoint_round(round_loop: Dict[str, Any]) -> Optional[int]:
    return next_checkpoint_round(round_loop, context_compression_interval())


def display_update_interval() -> int:
    return 5


def latest_display_update_round(round_loop: Dict[str, Any]) -> Optional[int]:
    return checkpoint_round(round_loop, display_update_interval())


def next_display_update_round(round_loop: Dict[str, Any]) -> Optional[int]:
    return next_checkpoint_round(round_loop, display_update_interval())


def display_update_due(round_loop: Dict[str, Any]) -> bool:
    completed = int(round_loop.get('completed_rounds', 0) or 0)
    interval = display_update_interval()
    return completed > 0 and completed % interval == 0 and round_loop.get('current_round_index') is None


def supervisor_watchdog_timeout_minutes() -> int:
    return 10


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
            'node_a must run outside the LLM sandbox because it requires direct CUDA / Nsight Compute access; '
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


def existing_files_in_scope(paths: Sequence[Path | str]) -> List[Path]:
    existing: List[Path] = []
    seen: set[Path] = set()
    for raw_path in paths:
        path = Path(raw_path)
        if not path.exists():
            continue
        if path.is_dir():
            for child in sorted(path.rglob('*')):
                if child.is_file() and child not in seen:
                    existing.append(child)
                    seen.add(child)
            continue
        if path.is_file() and path not in seen:
            existing.append(path)
            seen.add(path)
    return existing


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


def resolve_repo_path(path_str: Optional[str]) -> Optional[Path]:
    if not path_str:
        return None
    path = Path(path_str)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def repo_rel_run_artifact(run_dir: Path, raw_path: Optional[str]) -> Optional[str]:
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


def relativize_ncu_summary_paths(run_dir: Path, payload: Dict[str, Any]) -> Dict[str, Any]:
    summary = copy.deepcopy(payload)
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
            summary[key] = repo_rel_run_artifact(run_dir, summary.get(key))

    artifacts = summary.get('artifacts')
    if isinstance(artifacts, dict):
        for artifact in artifacts.values():
            if not isinstance(artifact, dict):
                continue
            if 'path' in artifact:
                artifact['path'] = repo_rel_run_artifact(run_dir, artifact.get('path'))
            if 'legacy_alias_path' in artifact:
                artifact['legacy_alias_path'] = repo_rel_run_artifact(run_dir, artifact.get('legacy_alias_path'))
    return summary


def summarize_run(
    run_dir: Path,
    measured_commit: Optional[str],
    benchmark_state: Dict[str, Any],
) -> tuple[Dict[str, Any], Dict[str, Any], bool]:
    raw_summary = load_json_file(run_dir / 'summary.json')
    analysis_path = run_dir / 'ncu_analysis.json'
    ncu_summary_path = run_dir / 'ncu_summary.json'
    if analysis_path.exists():
        analysis = load_json_file(analysis_path)
        raw_ncu = ncu_analysis.build_rich_summary_from_analysis(analysis)
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
        'ncu_analysis_path': repo_rel(analysis_path) if analysis_path.exists() else None,
        'ncu_summary_json': repo_rel(LATEST_NCU_SUMMARY_PATH),
        'is_new_best_custom': is_new_best,
        'measured_commit': measured_commit,
        'generated_at': now_local_iso(),
    }

    raw_ncu = relativize_ncu_summary_paths(run_dir, raw_ncu)
    latest_ncu = {
        'schema_version': raw_ncu.get('schema_version', 2),
        'status': raw_ncu.get('status', 'missing'),
        'source_run_id': run_id,
        'source_run_dir': repo_rel(run_dir),
        'analysis_path': repo_rel(analysis_path) if analysis_path.exists() else raw_ncu.get('analysis_path'),
        'kernel_name': raw_ncu.get('kernel_name'),
        'block_size': raw_ncu.get('block_size'),
        'grid_size': raw_ncu.get('grid_size'),
        'registers_per_thread': raw_ncu.get('registers_per_thread'),
        'shared_mem_per_block_allocated': raw_ncu.get('shared_mem_per_block_allocated'),
        'launch': raw_ncu.get(
            'launch',
            {
                'kernel_name': raw_ncu.get('kernel_name'),
                'block_size': raw_ncu.get('block_size'),
                'grid_size': raw_ncu.get('grid_size'),
                'registers_per_thread': raw_ncu.get('registers_per_thread'),
                'shared_mem_per_block_allocated': raw_ncu.get('shared_mem_per_block_allocated'),
            },
        ),
        'headline_metrics': raw_ncu.get('headline_metrics', {}),
        'stall_breakdown': raw_ncu.get('stall_breakdown', []),
        'bottleneck_classes': raw_ncu.get('bottleneck_classes', []),
        'top_findings': raw_ncu.get('top_findings', []),
        'top_source_hotspots': raw_ncu.get('top_source_hotspots', []),
        'handoff': raw_ncu.get(
            'handoff',
            {
                'node_b': {'top_findings': [], 'code_regions_to_investigate': []},
                'node_c': {'target_hotspots': [], 'guardrail_metrics': [], 'expected_recheck_points': []},
            },
        ),
        'delta_vs_previous_run': raw_ncu.get(
            'delta_vs_previous_run',
            {
                'baseline_run_id': None,
                'headline_metrics': {},
                'stall_breakdown': [],
                'source_hotspots': {'improved': [], 'regressed': [], 'new': [], 'disappeared': []},
            },
        ),
        'raw_csv_path': raw_ncu.get('raw_csv_path') or (repo_rel(run_dir / 'ncu_metrics.csv') if (run_dir / 'ncu_metrics.csv').exists() else None),
        'raw_rep_path': raw_ncu.get('raw_rep_path') or (repo_rel(run_dir / 'ncu_profile.ncu-rep') if (run_dir / 'ncu_profile.ncu-rep').exists() else None),
        'raw_details_csv_path': raw_ncu.get('raw_details_csv_path') or (repo_rel(run_dir / 'ncu_details.csv') if (run_dir / 'ncu_details.csv').exists() else None),
        'import_raw_csv_path': raw_ncu.get('import_raw_csv_path'),
        'details_page_csv_path': raw_ncu.get('details_page_csv_path'),
        'source_csv_path': raw_ncu.get('source_csv_path'),
        'artifacts': raw_ncu.get('artifacts', {}),
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
    return compute_gap_from_entries(custom, cutlass)


def compute_gap_from_entries(
    custom_entry: Dict[str, Any],
    baseline_entry: Dict[str, Any],
) -> tuple[Optional[float], Optional[float]]:
    custom_runtime = custom_entry.get('median_runtime_ms')
    baseline_runtime = baseline_entry.get('median_runtime_ms')
    if baseline_runtime is None or custom_runtime is None:
        return None, None
    absolute = float(custom_runtime) - float(baseline_runtime)
    ratio = float(custom_runtime) / float(baseline_runtime) if float(baseline_runtime) else None
    return absolute, ratio


def format_runtime_ratio_text(runtime_ratio: float, baseline_label: str) -> str:
    relation = 'faster' if runtime_ratio < 1.0 else 'slower' if runtime_ratio > 1.0 else 'matched'
    return f"`{runtime_ratio:.6f}x` of {baseline_label} runtime ({relation})"


def default_goal_summary() -> str:
    return 'Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.'


def project_goal_summary(search_state: Dict[str, Any]) -> str:
    summary = str(search_state.get('goal_summary') or '').strip()
    return summary or default_goal_summary()


def format_project_goal_details(search_state: Dict[str, Any]) -> list[str]:
    details: list[str] = []
    target_runtime = parse_priority(search_state.get('target_runtime_ms'))
    target_competitor = str(search_state.get('target_competitor') or '').strip()
    if target_runtime is not None:
        details.append(f"target runtime: `<= {target_runtime:.3f} ms`")
    if target_competitor:
        details.append(f"comparison target: `{target_competitor}`")
    baseline_run_id = search_state.get('bootstrap_baseline_run_id')
    baseline_runtime = parse_priority(search_state.get('bootstrap_baseline_runtime_ms'))
    baseline_commit = search_state.get('bootstrap_baseline_measured_commit')
    if baseline_run_id or baseline_commit or baseline_runtime is not None:
        details.append(
            "rebootstrap source: "
            + f"`{baseline_run_id or 'N/A'}`"
            + (
                f", commit `{baseline_commit}`"
                if baseline_commit
                else ''
            )
            + (
                f", historical runtime `{fmt_runtime(baseline_runtime)}`"
                if baseline_runtime is not None
                else ''
            )
        )
    return details


def build_rebootstrap_goal_summary(
    *,
    goal_summary: Optional[str],
    goal_runtime_ms: Optional[float],
    goal_competitor: Optional[str],
) -> str:
    if goal_summary and goal_summary.strip():
        return goal_summary.strip()
    runtime = parse_priority(goal_runtime_ms)
    competitor = str(goal_competitor or '').strip()
    if competitor and runtime is not None:
        return (
            f"Beat {competitor} and drive the fixed-shape BF16 GEMM "
            f"`fixed_bf16_gemm_v1` to `<= {runtime:.3f} ms`."
        )
    if competitor:
        return f"Beat {competitor} on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`."
    if runtime is not None:
        return f"Drive the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1` to `<= {runtime:.3f} ms`."
    return default_goal_summary()


def parse_priority(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def has_meaningful_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return True


def frontier_policy(search_state: Dict[str, Any]) -> Dict[str, Any]:
    policy = dict(search_state.get('selection_policy') or {})
    policy.setdefault('policy_id', 'family_representative_v2')
    policy.setdefault('allow_restore_base', True)
    policy.setdefault('max_open_candidates', 3)
    policy.setdefault('max_reopens_per_candidate', 1)
    policy.setdefault('reopen_loss_tolerance_ms', 0.15)
    policy.setdefault('reopen_fail_risk_ceiling', 0.6)
    policy.setdefault('family_representatives_only', True)
    return policy


def candidate_family_key(candidate: Dict[str, Any]) -> str:
    return str(
        candidate.get('family_id')
        or candidate.get('subfamily_id')
        or candidate.get('candidate_id')
        or 'family::unknown'
    ).strip()


def candidate_status_from_transition_label(transition_label: Optional[str]) -> str:
    if transition_label == 'PASS_WIN':
        return 'measured_win'
    if transition_label == 'PASS_FLAT':
        return 'measured_flat'
    if transition_label in ('PASS_LOSS', 'DIAG_POS_RUNTIME_NEG'):
        return 'measured_loss'
    if transition_label == 'BUILD_FAIL':
        return 'build_failed'
    if transition_label == 'CORRECTNESS_FAIL':
        return 'correctness_failed'
    return 'closed'


def candidate_summary_from_record(candidate: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'direction_id': candidate.get('direction_id'),
        'name': candidate.get('direction_name') or candidate.get('name'),
        'family_id': candidate.get('family_id'),
        'subfamily_id': candidate.get('subfamily_id'),
        'action_fingerprint': candidate.get('action_fingerprint'),
        'mode': candidate.get('mode'),
        'hypothesis': candidate.get('hypothesis'),
        'expected_bottleneck': candidate.get('expected_bottleneck'),
        'code_locations': normalize_string_list(candidate.get('code_locations')),
        'risk': candidate.get('risk'),
        'metrics_to_recheck': normalize_string_list(candidate.get('metrics_to_recheck')),
        'search_score_v1': candidate.get('search_score_v1'),
        'score_breakdown': dict(candidate.get('score_breakdown') or {}),
        'predicted_gain_ms': candidate.get('predicted_gain_ms'),
        'predicted_fail_risk': candidate.get('predicted_fail_risk'),
        'ranking_notes': normalize_string_list(candidate.get('ranking_notes')),
        'stop_condition': candidate.get('stop_condition'),
        'evidence_refs': normalize_string_list(candidate.get('evidence_refs')),
        'target_hotspots': normalize_dict_list(candidate.get('target_hotspots')),
        'expected_local_changes': normalize_string_list(candidate.get('expected_local_changes')),
        'guardrail_metrics': normalize_dict_list(candidate.get('guardrail_metrics')),
        'idea_origin': candidate.get('idea_origin', 'auto-analysis'),
    }


def frontier_candidate_defaults(candidate_id: Optional[str]) -> Dict[str, Any]:
    return {
        'candidate_id': candidate_id,
        'source_diagnosis_id': None,
        'base_run_id': None,
        'base_measured_commit': None,
        'base_runtime_ms': None,
        'direction_id': None,
        'direction_name': None,
        'family_id': None,
        'subfamily_id': None,
        'action_fingerprint': None,
        'rank_in_diagnosis': None,
        'recommended': False,
        'mode': None,
        'priority': None,
        'search_score_v1': None,
        'score_breakdown': {},
        'predicted_gain_ms': None,
        'predicted_fail_risk': None,
        'ranking_notes': [],
        'hypothesis': None,
        'expected_bottleneck': None,
        'code_locations': [],
        'risk': None,
        'metrics_to_recheck': [],
        'stop_condition': None,
        'evidence_refs': [],
        'target_hotspots': [],
        'expected_local_changes': [],
        'guardrail_metrics': [],
        'status': 'open',
        'source_search_iteration': None,
        'selection_count': 0,
        'reopen_count': 0,
        'last_selected_at': None,
        'last_selected_selection_mode': None,
        'last_transition_label': None,
        'last_transition_class': None,
        'last_result_run_id': None,
        'last_result_runtime_ms': None,
        'last_runtime_delta_ms': None,
        'last_result_correctness_passed': None,
        'last_closed_at': None,
        'last_closed_search_iteration': None,
        'last_reopened_search_iteration': None,
        'reopened_at': None,
        'is_family_representative': False,
        'family_representative_score': None,
        'family_representative_reason': None,
        'invalid_reason': None,
        'notes': None,
    }


def merge_missing_candidate_fields(target: Dict[str, Any], source: Dict[str, Any]) -> bool:
    changed = False
    for key in (
        'source_diagnosis_id',
        'base_run_id',
        'base_measured_commit',
        'base_runtime_ms',
        'direction_id',
        'direction_name',
        'family_id',
        'subfamily_id',
        'action_fingerprint',
        'rank_in_diagnosis',
        'recommended',
        'mode',
        'priority',
        'search_score_v1',
        'score_breakdown',
        'predicted_gain_ms',
        'predicted_fail_risk',
        'ranking_notes',
        'hypothesis',
        'expected_bottleneck',
        'code_locations',
        'risk',
        'metrics_to_recheck',
        'stop_condition',
        'evidence_refs',
        'target_hotspots',
        'expected_local_changes',
        'guardrail_metrics',
    ):
        if not has_meaningful_value(target.get(key)) and has_meaningful_value(source.get(key)):
            target[key] = copy.deepcopy(source.get(key))
            changed = True
    return changed


def normalize_frontier_candidate(raw_candidate: Dict[str, Any]) -> Dict[str, Any]:
    candidate = frontier_candidate_defaults(str(raw_candidate.get('candidate_id') or '').strip() or None)
    candidate.update(copy.deepcopy(raw_candidate))

    candidate['candidate_id'] = str(candidate.get('candidate_id') or '').strip() or None
    candidate['source_diagnosis_id'] = str(candidate.get('source_diagnosis_id') or '').strip() or None
    candidate['direction_id'] = str(candidate.get('direction_id') or '').strip() or None
    candidate['direction_name'] = str(candidate.get('direction_name') or candidate.get('name') or '').strip() or None
    candidate['family_id'] = str(candidate.get('family_id') or '').strip() or None
    candidate['subfamily_id'] = str(candidate.get('subfamily_id') or candidate.get('family_id') or '').strip() or candidate['family_id']
    candidate['action_fingerprint'] = str(candidate.get('action_fingerprint') or '').strip() or None
    candidate['mode'] = str(candidate.get('mode') or '').strip() or None
    candidate['hypothesis'] = str(candidate.get('hypothesis') or '').strip() or None
    candidate['expected_bottleneck'] = str(candidate.get('expected_bottleneck') or '').strip() or None
    candidate['risk'] = str(candidate.get('risk') or '').strip() or None
    candidate['stop_condition'] = str(candidate.get('stop_condition') or '').strip() or None
    candidate['notes'] = str(candidate.get('notes') or '').strip() or None
    candidate['recommended'] = bool(candidate.get('recommended'))
    candidate['score_breakdown'] = dict(candidate.get('score_breakdown') or {})
    candidate['ranking_notes'] = normalize_string_list(candidate.get('ranking_notes'))
    candidate['code_locations'] = normalize_string_list(candidate.get('code_locations'))
    candidate['metrics_to_recheck'] = normalize_string_list(candidate.get('metrics_to_recheck'))
    candidate['evidence_refs'] = normalize_string_list(candidate.get('evidence_refs'))
    candidate['target_hotspots'] = normalize_dict_list(candidate.get('target_hotspots'))
    candidate['expected_local_changes'] = normalize_string_list(candidate.get('expected_local_changes'))
    candidate['guardrail_metrics'] = normalize_dict_list(candidate.get('guardrail_metrics'))

    priority = parse_priority(candidate.get('priority'))
    search_score = parse_priority(candidate.get('search_score_v1'))
    if priority is None and search_score is None:
        priority = fallback_search_score_v1(
            candidate.get('rank_in_diagnosis', 99),
            candidate.get('recommended'),
            candidate.get('risk'),
        )
        search_score = priority
    elif priority is None:
        priority = search_score
    elif search_score is None:
        search_score = priority
    candidate['priority'] = priority
    candidate['search_score_v1'] = search_score
    candidate['predicted_gain_ms'] = parse_priority(candidate.get('predicted_gain_ms'))
    candidate['predicted_fail_risk'] = parse_priority(candidate.get('predicted_fail_risk'))
    candidate['base_runtime_ms'] = parse_priority(candidate.get('base_runtime_ms'))
    candidate['last_result_runtime_ms'] = parse_priority(candidate.get('last_result_runtime_ms'))
    candidate['last_runtime_delta_ms'] = parse_priority(candidate.get('last_runtime_delta_ms'))
    candidate['family_representative_score'] = parse_priority(candidate.get('family_representative_score'))

    status = str(candidate.get('status') or 'open').strip() or 'open'
    if status not in {
        'open',
        'parked',
        'selected',
        'reopened',
        'measured_win',
        'measured_flat',
        'measured_loss',
        'build_failed',
        'correctness_failed',
        'invalid',
        'duplicate',
        'closed',
    }:
        status = 'open'
    candidate['status'] = status
    candidate['selection_count'] = int(candidate.get('selection_count') or 0)
    candidate['reopen_count'] = int(candidate.get('reopen_count') or 0)
    candidate['source_search_iteration'] = (
        int(candidate['source_search_iteration'])
        if candidate.get('source_search_iteration') is not None
        else None
    )
    candidate['last_closed_search_iteration'] = (
        int(candidate['last_closed_search_iteration'])
        if candidate.get('last_closed_search_iteration') is not None
        else None
    )
    candidate['last_reopened_search_iteration'] = (
        int(candidate['last_reopened_search_iteration'])
        if candidate.get('last_reopened_search_iteration') is not None
        else None
    )
    candidate['is_family_representative'] = bool(candidate.get('is_family_representative'))
    candidate['invalid_reason'] = str(candidate.get('invalid_reason') or '').strip() or None
    candidate['family_representative_reason'] = str(candidate.get('family_representative_reason') or '').strip() or None
    candidate['last_transition_label'] = str(candidate.get('last_transition_label') or '').strip() or None
    candidate['last_transition_class'] = str(candidate.get('last_transition_class') or '').strip() or None
    return candidate


def normalize_search_frontier(frontier: Dict[str, Any]) -> bool:
    changed = False
    if frontier.get('schema_version') != 2:
        frontier['schema_version'] = 2
        changed = True
    if frontier.get('frontier_id') != 'frontier:global':
        frontier['frontier_id'] = 'frontier:global'
        changed = True
    if frontier.get('selection_policy_id') != 'family_representative_v2':
        frontier['selection_policy_id'] = 'family_representative_v2'
        changed = True
    for key, default in (
        ('updated_at', None),
        ('family_representative_count', 0),
        ('reopened_candidate_ids', []),
        ('selected_candidate_id', None),
        ('selection_reason', None),
        ('selection_summary', None),
    ):
        if key not in frontier:
            frontier[key] = copy.deepcopy(default)
            changed = True

    search_candidates = load_search_candidates()
    candidate_lookup = {
        candidate.get('candidate_id'): candidate
        for candidate in search_candidates.get('candidates', [])
        if candidate.get('candidate_id')
    }

    normalized_candidates: List[Dict[str, Any]] = []
    for raw_candidate in frontier.get('candidates', []):
        candidate = copy.deepcopy(raw_candidate)
        candidate_id = candidate.get('candidate_id')
        if candidate_id in candidate_lookup:
            changed = merge_missing_candidate_fields(candidate, candidate_lookup[candidate_id]) or changed
        normalized = normalize_frontier_candidate(candidate)
        if normalized != raw_candidate:
            changed = True
        normalized_candidates.append(normalized)
    if normalized_candidates != frontier.get('candidates', []):
        frontier['candidates'] = normalized_candidates
        changed = True
    return changed


def frontier_candidate_lookup(
    frontier: Dict[str, Any],
    candidate_id: Optional[str] = None,
    *,
    direction_id: Optional[str] = None,
    source_diagnosis_id: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    for candidate in frontier.get('candidates', []):
        if candidate_id and candidate.get('candidate_id') != candidate_id:
            continue
        if direction_id and candidate.get('direction_id') != direction_id:
            continue
        if source_diagnosis_id and candidate.get('source_diagnosis_id') != source_diagnosis_id:
            continue
        return candidate
    return None


def mark_frontier_candidate_closed(
    frontier: Dict[str, Any],
    candidate_id: Optional[str],
    *,
    transition_label: str,
    transition_class: Optional[str],
    result_run_id: Optional[str],
    result_runtime_ms: Optional[float],
    runtime_delta_ms: Optional[float],
    correctness_passed: Optional[bool],
    close_reason: str,
    search_iteration: Optional[int],
) -> bool:
    if not candidate_id:
        return False
    candidate = frontier_candidate_lookup(frontier, candidate_id)
    if candidate is None:
        return False
    changed = False
    desired_status = candidate_status_from_transition_label(transition_label)
    for key, value in (
        ('status', desired_status),
        ('last_transition_label', transition_label),
        ('last_transition_class', transition_class),
        ('last_result_run_id', result_run_id),
        ('last_result_runtime_ms', result_runtime_ms),
        ('last_runtime_delta_ms', runtime_delta_ms),
        ('last_result_correctness_passed', correctness_passed),
        ('last_closed_at', now_local_iso()),
        ('last_closed_search_iteration', search_iteration),
        ('invalid_reason', close_reason),
    ):
        if candidate.get(key) != value:
            candidate[key] = value
            changed = True
    if frontier.get('selected_candidate_id') == candidate_id:
        frontier['selected_candidate_id'] = None
        frontier['selection_reason'] = None
        frontier['selection_summary'] = (
            f"Candidate {candidate_id} closed via {transition_label.lower()} after selection."
        )
        changed = True
    return changed


def reconcile_frontier_with_latest_attempt(frontier: Dict[str, Any]) -> bool:
    latest_attempt = load_latest_attempt()
    candidate_id = latest_attempt.get('candidate_id')
    if not candidate_id:
        return False
    transition_label = latest_attempt.get('transition_label')
    if transition_label:
        return mark_frontier_candidate_closed(
            frontier,
            candidate_id,
            transition_label=transition_label,
            transition_class=latest_attempt.get('transition_class'),
            result_run_id=(latest_attempt.get('measurement') or {}).get('run_id'),
            result_runtime_ms=parse_priority((latest_attempt.get('measurement') or {}).get('runtime_ms')),
            runtime_delta_ms=parse_priority((latest_attempt.get('measurement') or {}).get('runtime_delta_ms')),
            correctness_passed=(latest_attempt.get('measurement') or {}).get('correctness'),
            close_reason=str(latest_attempt.get('close_reason') or 'reconciled_from_latest_attempt'),
            search_iteration=load_search_state().get('search_iteration'),
        )
    if str(latest_attempt.get('build_status') or '').upper() == 'FAIL':
        return mark_frontier_candidate_closed(
            frontier,
            candidate_id,
            transition_label='BUILD_FAIL',
            transition_class='fail',
            result_run_id=None,
            result_runtime_ms=None,
            runtime_delta_ms=None,
            correctness_passed=None,
            close_reason='build_failed_by_node_c',
            search_iteration=load_search_state().get('search_iteration'),
        )
    return False


def candidate_effective_priority(
    candidate: Dict[str, Any],
    family_entry: Dict[str, Any],
    search_state: Dict[str, Any],
) -> float:
    score = parse_priority(candidate.get('priority'))
    if score is None:
        score = fallback_search_score_v1(
            candidate.get('rank_in_diagnosis', 99),
            candidate.get('recommended'),
            candidate.get('risk'),
        )
    current_iteration = int(search_state.get('search_iteration') or 0)
    source_iteration = candidate.get('source_search_iteration')
    if source_iteration is not None:
        freshness = max(0.0, 0.15 - 0.03 * max(current_iteration - int(source_iteration), 0))
        score += freshness
    if candidate.get('recommended'):
        score += 0.1
    predicted_fail_risk = parse_priority(candidate.get('predicted_fail_risk')) or 0.0
    score -= min(max(predicted_fail_risk, 0.0), 1.0) * 0.25

    transition_label = candidate.get('last_transition_label')
    if transition_label == 'PASS_FLAT':
        score -= 0.25
    elif transition_label in ('PASS_LOSS', 'DIAG_POS_RUNTIME_NEG'):
        runtime_delta_ms = abs(parse_priority(candidate.get('last_runtime_delta_ms')) or 0.0)
        score -= 0.35 + min(runtime_delta_ms, 0.25) * 2.0
    elif transition_label == 'BUILD_FAIL':
        score -= 1.0
    elif transition_label == 'CORRECTNESS_FAIL':
        score -= 1.25

    score -= min(int(candidate.get('reopen_count') or 0), 3) * 0.15
    score -= min(int(family_entry.get('losses', 0) or 0), 4) * 0.08
    score -= min(int(family_entry.get('fails', 0) or 0), 3) * 0.2
    if candidate.get('status') == 'reopened':
        score -= 0.05
    return score


def candidate_reopen_eligible(
    candidate: Dict[str, Any],
    family_entry: Dict[str, Any],
    search_state: Dict[str, Any],
) -> bool:
    if candidate.get('status') not in {'measured_flat', 'measured_loss', 'closed'}:
        return False
    policy = frontier_policy(search_state)
    if int(candidate.get('reopen_count') or 0) >= int(policy.get('max_reopens_per_candidate', 1)):
        return False
    closed_iteration = candidate.get('last_closed_search_iteration')
    current_iteration = int(search_state.get('search_iteration') or 0)
    if closed_iteration is not None and current_iteration <= int(closed_iteration):
        return False
    if int(family_entry.get('fails', 0) or 0) > 0:
        return False
    if int(family_entry.get('losses', 0) or 0) > 2:
        return False

    transition_label = candidate.get('last_transition_label')
    if transition_label == 'PASS_FLAT':
        return True
    if transition_label not in ('PASS_LOSS', 'DIAG_POS_RUNTIME_NEG'):
        return False

    runtime_delta_ms = abs(parse_priority(candidate.get('last_runtime_delta_ms')) or 1e9)
    predicted_gain_ms = abs(parse_priority(candidate.get('predicted_gain_ms')) or 0.0)
    predicted_fail_risk = parse_priority(candidate.get('predicted_fail_risk')) or 1.0
    loss_tolerance_ms = max(
        float(policy.get('reopen_loss_tolerance_ms', 0.15)),
        predicted_gain_ms,
    )
    fail_risk_ceiling = float(policy.get('reopen_fail_risk_ceiling', 0.6))
    return runtime_delta_ms <= loss_tolerance_ms and predicted_fail_risk <= fail_risk_ceiling


def refresh_frontier_family_representatives(
    frontier: Dict[str, Any],
    search_state: Dict[str, Any],
    family_ledger: Dict[str, Any],
) -> bool:
    changed = False
    families = family_ledger.get('families') or {}
    reopened_candidate_ids: List[str] = []
    members_by_family: Dict[str, List[Dict[str, Any]]] = {}

    for candidate in frontier.get('candidates', []):
        if candidate.get('is_family_representative'):
            candidate['is_family_representative'] = False
            changed = True
        if candidate.get('family_representative_score') is not None:
            candidate['family_representative_score'] = None
            changed = True
        if candidate.get('family_representative_reason') is not None:
            candidate['family_representative_reason'] = None
            changed = True
        members_by_family.setdefault(candidate_family_key(candidate), []).append(candidate)

    representative_count = 0
    current_iteration = int(search_state.get('search_iteration') or 0)
    for family_id, members in members_by_family.items():
        family_entry = dict(family_ledger_entry_defaults(family_id))
        family_entry.update(families.get(family_id, {}))
        contenders: List[tuple[float, Dict[str, Any], bool]] = []
        for candidate in members:
            status = candidate.get('status')
            reopen_eligible = candidate_reopen_eligible(candidate, family_entry, search_state)
            if status not in {'open', 'parked', 'reopened', 'selected'} and not reopen_eligible:
                continue
            contenders.append(
                (
                    candidate_effective_priority(candidate, family_entry, search_state),
                    candidate,
                    reopen_eligible,
                )
            )
        if not contenders:
            continue

        contenders.sort(
            key=lambda item: (
                -item[0],
                frontier_sort_key(item[1]),
            )
        )
        best_score, best_candidate, best_is_reopen = contenders[0]
        representative_count += 1

        if best_is_reopen and best_candidate.get('status') not in {'open', 'reopened', 'selected'}:
            if best_candidate.get('last_reopened_search_iteration') != current_iteration:
                best_candidate['reopen_count'] = int(best_candidate.get('reopen_count') or 0) + 1
                best_candidate['last_reopened_search_iteration'] = current_iteration
                best_candidate['reopened_at'] = now_local_iso()
            if best_candidate.get('status') != 'reopened':
                best_candidate['status'] = 'reopened'
            reopened_candidate_ids.append(best_candidate.get('candidate_id'))
            changed = True
        elif best_candidate.get('status') == 'parked':
            best_candidate['status'] = 'open'
            changed = True

        if not best_candidate.get('is_family_representative'):
            best_candidate['is_family_representative'] = True
            changed = True
        representative_score = round(best_score, 6)
        if best_candidate.get('family_representative_score') != representative_score:
            best_candidate['family_representative_score'] = representative_score
            changed = True
        representative_reason = (
            'historical_reopen_representative'
            if best_is_reopen
            else 'best_family_candidate_after_reorder'
        )
        if best_candidate.get('family_representative_reason') != representative_reason:
            best_candidate['family_representative_reason'] = representative_reason
            changed = True

        for candidate in members:
            if candidate is best_candidate:
                continue
            if candidate.get('status') in {'open', 'reopened'}:
                candidate['status'] = 'parked'
                changed = True

    if frontier.get('family_representative_count') != representative_count:
        frontier['family_representative_count'] = representative_count
        changed = True
    if frontier.get('reopened_candidate_ids') != reopened_candidate_ids:
        frontier['reopened_candidate_ids'] = reopened_candidate_ids
        changed = True
    status = 'ready' if representative_count else 'empty'
    if frontier.get('status') != status:
        frontier['status'] = status
        changed = True
    updated_at = now_local_iso()
    if frontier.get('updated_at') != updated_at:
        frontier['updated_at'] = updated_at
        changed = True
    notes = (
        f"Persistent frontier tracks {len(frontier.get('candidates', []))} historical candidates; "
        f"{representative_count} family representatives are currently active for selection."
    )
    if frontier.get('notes') != notes:
        frontier['notes'] = notes
        changed = True
    return changed


def frontier_sort_key(candidate: Dict[str, Any]) -> tuple[float, int, str, str]:
    priority = parse_priority(candidate.get('family_representative_score'))
    if priority is None:
        priority = parse_priority(candidate.get('priority'))
    rank_bias = 0 if candidate.get('recommended') else 1
    return (
        -(priority if priority is not None else float('-inf')),
        rank_bias,
        str(candidate.get('direction_id') or ''),
        str(candidate.get('candidate_id') or ''),
    )


def candidate_invalid_reason(candidate: Dict[str, Any], diagnosis: Dict[str, Any]) -> Optional[str]:
    if candidate.get('status') not in {'open', 'reopened'}:
        return 'not_open'
    if not str(candidate.get('candidate_id') or '').strip():
        return 'missing_candidate_id'
    if not str(candidate.get('direction_id') or '').strip():
        return 'missing_direction_id'
    if not str(candidate.get('direction_name') or '').strip():
        return 'missing_direction_name'
    if not str(candidate.get('family_id') or '').strip():
        return 'missing_family_id'
    if not str(candidate.get('action_fingerprint') or '').strip():
        return 'missing_action_fingerprint'
    if parse_priority(candidate.get('priority')) is None:
        return 'non_numeric_priority'
    if not str(candidate.get('hypothesis') or '').strip():
        return 'missing_hypothesis'
    if not normalize_string_list(candidate.get('code_locations')):
        return 'missing_code_locations'
    return None


def frontier_open_candidates(frontier: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates = [
        candidate
        for candidate in frontier.get('candidates', [])
        if candidate.get('status') in {'open', 'reopened'}
    ]
    return sorted(candidates, key=frontier_sort_key)


def selectable_frontier_candidates(frontier: Dict[str, Any], diagnosis: Dict[str, Any]) -> List[Dict[str, Any]]:
    selected: List[Dict[str, Any]] = []
    seen_fingerprints: set[str] = set()
    for candidate in frontier_open_candidates(frontier):
        reason = candidate_invalid_reason(candidate, diagnosis)
        fingerprint = str(candidate.get('action_fingerprint') or '').strip()
        if reason is not None:
            continue
        if not candidate.get('is_family_representative'):
            continue
        if fingerprint in seen_fingerprints:
            continue
        selected.append(candidate)
        seen_fingerprints.add(fingerprint)
    return selected


def best_frontier_candidate(frontier: Dict[str, Any], diagnosis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    candidates = selectable_frontier_candidates(frontier, diagnosis)
    return candidates[0] if candidates else None


def direction_summary_line(direction: Dict[str, Any]) -> str:
    name = direction.get('name') or 'PENDING'
    bottleneck = direction.get('expected_bottleneck') or 'PENDING'
    return (
        f"{direction.get('direction_id', 'dir_xx')}: "
        f"{name} | "
        f"bottleneck: {bottleneck}"
    )


def active_direction_summary(
    active_direction: Dict[str, Any],
    diagnosis: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    summary = active_direction.get('summary')
    if isinstance(summary, dict) and summary:
        return summary
    if diagnosis is not None:
        direction = direction_lookup(diagnosis, active_direction.get('direction_id') or '')
        if direction is not None:
            return direction
    return {}


def normalize_dict_list(values: Any) -> List[Dict[str, Any]]:
    if not isinstance(values, list):
        return []
    normalized: List[Dict[str, Any]] = []
    for value in values:
        if isinstance(value, dict):
            normalized.append(copy.deepcopy(value))
    return normalized


def sibling_repo_path(path_str: Optional[str], new_name: Optional[str] = None, suffix: Optional[str] = None) -> Optional[str]:
    path = resolve_repo_path(path_str)
    if path is None:
        return None
    if new_name is not None:
        path = path.with_name(new_name)
    if suffix is not None:
        path = path.with_suffix(suffix)
    return repo_rel(path)


def format_top_finding(item: Dict[str, Any]) -> str:
    summary = str(item.get('summary') or 'N/A').strip()
    evidence = item.get('evidence') or []
    if evidence:
        first = evidence[0] or {}
        evidence_ref = first.get('ref_id') or first.get('kind')
        if evidence_ref:
            return f"{summary} (evidence: {evidence_ref})"
    return summary


def format_hotspot_label(item: Dict[str, Any]) -> str:
    scope_type = item.get('scope_type') or 'unknown_scope'
    scope_name = item.get('scope_name') or 'unknown_scope_name'
    location = item.get('location') or 'N/A'
    metric_name = item.get('metric_name') or 'unknown_metric'
    metric_value = item.get('metric_value')
    explanation = item.get('explanation') or item.get('reason') or 'N/A'
    return (
        f"`{scope_type}` `{scope_name}` @ `{location}` | "
        f"`{metric_name}` = `{metric_value}` | {explanation}"
    )


def format_guardrail_label(item: Dict[str, Any]) -> str:
    return (
        f"`{item.get('metric_name', 'unknown_metric')}` "
        f"`{item.get('guardrail', 'observe')}` from `{item.get('current_value', 'N/A')}` | "
        f"{item.get('reason', 'N/A')}"
    )


def format_delta_hotspot_label(item: Dict[str, Any]) -> str:
    return (
        f"`{item.get('bucket', 'changed')}` `{item.get('scope_name') or item.get('location') or 'unknown_scope'}` | "
        f"`{item.get('metric_name', 'unknown_metric')}` | delta `{item.get('delta', 'N/A')}` | "
        f"trend `{item.get('trend', 'changed')}`"
    )


def format_evidence_label(item: Dict[str, Any]) -> str:
    if not isinstance(item, dict):
        return str(item)
    return (
        f"`{item.get('kind', 'evidence')}` `{item.get('ref_id', 'N/A')}` | "
        f"`{item.get('metric_name', 'N/A')}` = `{item.get('metric_value', 'N/A')}` | "
        f"{item.get('summary', 'N/A')}"
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
    lines.append(f"- ncu analysis path: `{latest_run.get('ncu_analysis_path', 'N/A')}`")
    lines.append(f"- measured commit: `{latest_run.get('measured_commit', 'N/A')}`")
    lines.append(f"- new best custom: `{'yes' if latest_run.get('is_new_best_custom') else 'no'}`")
    lines.append(f"- generated at: `{latest_run.get('generated_at', 'N/A')}`")
    return '\n'.join(lines) + '\n'


def render_latest_ncu_md(ncu_summary: Dict[str, Any]) -> str:
    launch = ncu_summary.get('launch') or {}
    delta_summary = ncu_summary.get('delta_vs_previous_run') or {}
    source_hotspot_deltas = delta_summary.get('source_hotspots') or {}
    node_b = (ncu_summary.get('handoff') or {}).get('node_b') or {}
    node_c = (ncu_summary.get('handoff') or {}).get('node_c') or {}
    artifacts = ncu_summary.get('artifacts') or {}

    lines = ['# Latest Nsight Compute summary', '']
    lines.append(f"- schema version: `{ncu_summary.get('schema_version', 'N/A')}`")
    lines.append(f"- source run id: `{ncu_summary.get('source_run_id', 'N/A')}`")
    lines.append(f"- source run dir: `{ncu_summary.get('source_run_dir', 'N/A')}`")
    lines.append(f"- status: `{ncu_summary.get('status', 'unknown')}`")
    lines.append(f"- analysis path: `{ncu_summary.get('analysis_path', 'N/A')}`")
    lines.append(f"- raw csv path: `{ncu_summary.get('raw_csv_path', 'N/A')}`")
    lines.append(f"- raw rep path: `{ncu_summary.get('raw_rep_path', 'N/A')}`")
    lines.append(f"- imported raw csv path: `{ncu_summary.get('import_raw_csv_path', 'N/A')}`")
    lines.append(f"- legacy import-raw alias path: `{ncu_summary.get('raw_details_csv_path', 'N/A')}`")
    lines.append(f"- details page csv path: `{ncu_summary.get('details_page_csv_path', 'N/A')}`")
    lines.append(f"- source page csv path: `{ncu_summary.get('source_csv_path', 'N/A')}`")
    lines.append('')
    lines.append('## Launch / kernel metadata')
    lines.append('')
    lines.append(f"- kernel name: `{launch.get('kernel_name', ncu_summary.get('kernel_name', 'N/A'))}`")
    lines.append(f"- block size: `{launch.get('block_size', ncu_summary.get('block_size', 'N/A'))}`")
    lines.append(f"- grid size: `{launch.get('grid_size', ncu_summary.get('grid_size', 'N/A'))}`")
    lines.append(f"- registers / thread: `{launch.get('registers_per_thread', ncu_summary.get('registers_per_thread', 'N/A'))}`")
    lines.append(
        f"- shared mem / block allocated: `{launch.get('shared_mem_per_block_allocated', ncu_summary.get('shared_mem_per_block_allocated', 'N/A'))}`"
    )
    lines.append('')
    lines.append('## Headline metrics')
    lines.append('')
    headline_metrics = ncu_summary.get('headline_metrics') or {}
    if headline_metrics:
        for key, value in headline_metrics.items():
            lines.append(f"- `{key}`: `{value}`")
    else:
        lines.append('No parsed headline metrics are available yet.')
    lines.append('')
    lines.append('## Primary bottlenecks')
    lines.append('')
    bottlenecks = ncu_summary.get('bottleneck_classes') or []
    if bottlenecks:
        for item in bottlenecks[:6]:
            lines.append(
                f"- `{item.get('class_id', 'unknown_bottleneck')}` | severity `{item.get('severity_score', 'N/A')}` | {item.get('summary', 'N/A')}"
            )
            for evidence in item.get('evidence', [])[:2]:
                lines.append(f"- evidence: {format_evidence_label(evidence)}")
    else:
        lines.append('No structured bottleneck classes are available.')
    lines.append('')
    lines.append('## Stall breakdown')
    lines.append('')
    stalls = ncu_summary.get('stall_breakdown') or []
    if stalls:
        for item in stalls:
            lines.append(
                f"- `{item.get('stall_group', 'unknown_stall')}`: `{item.get('metric_value', 'N/A')}` | {item.get('explanation', 'N/A')}"
            )
    else:
        lines.append('No structured stall breakdown is available.')
    lines.append('')
    lines.append('## Top hotspots')
    lines.append('')
    hotspots = ncu_summary.get('top_source_hotspots') or []
    if hotspots:
        for hotspot in hotspots[:8]:
            lines.append(f"- {format_hotspot_label(hotspot)}")
    else:
        source_page = artifacts.get('source_page') or {}
        lines.append('No source-level hotspots were produced.')
        if source_page.get('status') == 'unavailable':
            lines.append(f"- source page unavailable reason: `{source_page.get('unavailable_reason', 'unknown')}`")
    lines.append('')
    lines.append('## Delta vs previous run')
    lines.append('')
    lines.append(f"- baseline run id: `{delta_summary.get('baseline_run_id', 'N/A')}`")
    stall_deltas = delta_summary.get('stall_breakdown') or []
    if stall_deltas:
        for item in stall_deltas[:6]:
            lines.append(
                f"- stall `{item.get('stall_group', 'unknown_stall')}`: current `{item.get('current', 'N/A')}` vs previous `{item.get('previous', 'N/A')}` | delta `{item.get('delta', 'N/A')}` | trend `{item.get('trend', 'changed')}`"
            )
    else:
        lines.append('- no structured stall delta is available')
    delta_hotspots = ncu_analysis.top_hotspot_deltas(delta_summary)
    if delta_hotspots:
        for item in delta_hotspots[:6]:
            lines.append(f"- hotspot delta: {format_delta_hotspot_label(item)}")
    else:
        for bucket_name in ('regressed', 'new', 'improved', 'disappeared'):
            bucket = source_hotspot_deltas.get(bucket_name) or []
            if bucket:
                lines.append(f"- hotspot delta bucket `{bucket_name}` recorded with `{len(bucket)}` item(s)")
    lines.append('')
    lines.append('## Handoff to node_b')
    lines.append('')
    if node_b.get('top_findings'):
        for item in node_b.get('top_findings', [])[:6]:
            lines.append(f"- finding: {format_top_finding(item)}")
    else:
        lines.append('- no node_b findings were generated')
    if node_b.get('code_regions_to_investigate'):
        for item in node_b.get('code_regions_to_investigate', [])[:6]:
            lines.append(
                f"- investigate `{item.get('scope_type', 'region')}` `{item.get('scope_name', 'N/A')}` @ `{item.get('location', 'N/A')}` | {item.get('reason', 'N/A')}"
            )
    lines.append('')
    lines.append('## Handoff to node_c')
    lines.append('')
    if node_c.get('target_hotspots'):
        for item in node_c.get('target_hotspots', [])[:6]:
            lines.append(f"- target hotspot: {format_hotspot_label(item)}")
    else:
        lines.append('- no target hotspots were generated')
    if node_c.get('guardrail_metrics'):
        for item in node_c.get('guardrail_metrics', [])[:6]:
            lines.append(f"- guardrail: {format_guardrail_label(item)}")
    if node_c.get('expected_recheck_points'):
        for item in node_c.get('expected_recheck_points', [])[:6]:
            lines.append(
                f"- recheck `{item.get('scope_type', 'scope')}` `{item.get('scope_name', 'N/A')}` @ `{item.get('location', 'N/A')}` | `{item.get('metric_name', 'N/A')}` | {item.get('reason', 'N/A')}"
            )
    return '\n'.join(lines) + '\n'


def render_baseline_entry_md(lines: List[str], title: str, entry: Dict[str, Any]) -> None:
    lines.append(title)
    lines.append('')
    if not entry:
        lines.append('- status: NOT RECORDED')
        return
    lines.append('- status: RECORDED')
    lines.append(f"- kernel tag: `{entry.get('kernel_tag', 'N/A')}`")
    lines.append(f"- runtime: `{fmt_runtime(entry.get('median_runtime_ms'))}`")
    lines.append(f"- TFLOP/s: `{fmt_tflops(entry.get('tflops'))}`")
    lines.append(f"- correctness: `{'PASS' if entry.get('correctness_passed') else 'FAIL'}`")
    lines.append(f"- run dir: `{entry.get('run_dir', 'N/A')}`")
    lines.append(f"- summary json: `{entry.get('summary_json', 'N/A')}`")
    if entry.get('ncu_summary_json'):
        lines.append(f"- ncu summary json: `{entry.get('ncu_summary_json', 'N/A')}`")
    if entry.get('ncu_analysis_json'):
        lines.append(f"- ncu analysis json: `{entry.get('ncu_analysis_json', 'N/A')}`")
    if entry.get('ncu_analysis_md'):
        lines.append(f"- ncu analysis md: `{entry.get('ncu_analysis_md', 'N/A')}`")
    if entry.get('ncu_rep_path'):
        lines.append(f"- ncu rep path: `{entry.get('ncu_rep_path', 'N/A')}`")
    if entry.get('measured_commit'):
        lines.append(f"- measured commit: `{entry.get('measured_commit', 'N/A')}`")


def render_benchmark_baselines_md(benchmark_state: Dict[str, Any]) -> str:
    cutlass = benchmark_state.get('cutlass_baseline') or {}
    cublas = benchmark_state.get('cublas_baseline') or {}
    custom = benchmark_state.get('best_custom') or {}
    absolute_gap, runtime_ratio = compute_gap(benchmark_state)
    cublas_gap, cublas_ratio = compute_gap_from_entries(custom, cublas)

    lines = ['# Benchmark baselines', '', '## Official benchmark', '']
    lines.append(f"- dataset: `{benchmark_state.get('dataset_id', 'fixed_bf16_gemm_v1')}`")
    lines.append(f"- metric of record: `{benchmark_state.get('metric_of_record', 'median_runtime_ms')}`")
    lines.append('- correctness must pass before a performance result is accepted')
    lines.append('')
    render_baseline_entry_md(lines, '## CUTLASS baseline', cutlass)
    lines.append('')
    render_baseline_entry_md(lines, '## cuBLAS baseline', cublas)
    lines.append('')
    render_baseline_entry_md(lines, '## Best custom kernel', custom)
    lines.append('')
    lines.append('## Gap')
    lines.append('')
    if absolute_gap is None or runtime_ratio is None:
        lines.append('- gap vs CUTLASS: NOT AVAILABLE YET')
    else:
        lines.append(f"- absolute runtime gap vs CUTLASS: `{absolute_gap:.6f} ms`")
        lines.append(f"- runtime ratio vs CUTLASS: {format_runtime_ratio_text(runtime_ratio, 'CUTLASS')}")
    if cublas_gap is None or cublas_ratio is None:
        lines.append('- gap vs cuBLAS: NOT AVAILABLE YET')
    else:
        lines.append(f"- absolute runtime gap vs cuBLAS: `{cublas_gap:.6f} ms`")
        lines.append(f"- runtime ratio vs cuBLAS: {format_runtime_ratio_text(cublas_ratio, 'cuBLAS')}")
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
    lines.append(f"- auto select frontier: `{'yes' if round_loop.get('auto_select_frontier') else 'no'}`")
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
    search_state: Dict[str, Any],
    round_loop: Dict[str, Any],
) -> str:
    cutlass = benchmark_state.get('cutlass_baseline') or {}
    cublas = benchmark_state.get('cublas_baseline') or {}
    absolute_gap, runtime_ratio = compute_gap(benchmark_state)
    cublas_gap, cublas_ratio = compute_gap_from_entries(benchmark_state.get('best_custom') or {}, cublas)
    lines = ['# Progress', '', '## Objective', '']
    lines.append(project_goal_summary(search_state))
    for detail in format_project_goal_details(search_state):
        lines.append(f'- {detail}')
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
        lines.append(f"- current best custom gap: `{absolute_gap:.6f} ms`, {format_runtime_ratio_text(runtime_ratio, 'CUTLASS')}")
    else:
        lines.append('- current best custom gap: `N/A`')
    lines.append(f"- cuBLAS median runtime: `{fmt_runtime(cublas.get('median_runtime_ms'))}`")
    if cublas_gap is not None and cublas_ratio is not None:
        lines.append(f"- current best custom gap vs cuBLAS: `{cublas_gap:.6f} ms`, {format_runtime_ratio_text(cublas_ratio, 'cuBLAS')}")
    else:
        lines.append('- current best custom gap vs cuBLAS: `N/A`')
    return '\n'.join(lines) + '\n'


def render_current_focus_md(
    graph_state: Dict[str, Any],
    latest_run: Dict[str, Any],
    diagnosis: Dict[str, Any],
    active_direction: Dict[str, Any],
    search_state: Dict[str, Any],
    round_loop: Dict[str, Any],
) -> str:
    human_guidance_present = HUMAN_GUIDANCE_MD_PATH.exists() and bool(HUMAN_GUIDANCE_MD_PATH.read_text(encoding='utf-8').strip())
    lines = ['# Current focus', '']
    lines.append(f"- branch goal: `{project_goal_summary(search_state)}`")
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
    lines.append(
        f"- persistent human guidance: `{repo_rel(HUMAN_GUIDANCE_MD_PATH)}`"
        if human_guidance_present
        else '- persistent human guidance: `none recorded`'
    )
    lines.append(f"- immediate next action: `{graph_state.get('notes', 'Run status to inspect the current node')}`")
    return '\n'.join(lines) + '\n'


def render_human_review_md(
    graph_state: Dict[str, Any],
    diagnosis: Dict[str, Any],
    active_direction: Dict[str, Any],
    round_loop: Dict[str, Any],
) -> str:
    human_guidance = ''
    if HUMAN_GUIDANCE_MD_PATH.exists():
        human_guidance = HUMAN_GUIDANCE_MD_PATH.read_text(encoding='utf-8').strip()
    lines = ['# Human review queue', '', '## Current workflow gate', '']
    lines.append(f"- next node: `{graph_state.get('current_node', 'node_a')}`")
    lines.append(f"- status: `{graph_state.get('status', 'unknown')}`")
    lines.append(f"- round loop: `{round_label(round_loop)}` with `{round_loop.get('remaining_rounds', 0)}` rounds remaining")
    lines.append('')
    lines.append('## Direction approval policy')
    lines.append('')
    lines.append('- explicit approval: `python scripts/graph.py approve --direction dir_02`')
    lines.append('- select the top frontier candidate: `python scripts/graph.py select-next`')
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
    lines.append('')
    lines.append('## Persistent human guidance')
    lines.append('')
    lines.append('Read these items on every frontier-search / node_b ranking pass and map them into `family_audit`, diagnosis notes, or direction ranking when relevant.')
    lines.append('')
    if human_guidance:
        lines.extend(human_guidance.splitlines())
    else:
        lines.append('- no persistent human guidance recorded yet')
    return '\n'.join(lines) + '\n'


def render_node_b_context(
    graph_state: Dict[str, Any],
    latest_run: Dict[str, Any],
    ncu_summary: Dict[str, Any],
    diagnosis: Dict[str, Any],
    benchmark_state: Dict[str, Any],
    round_loop: Dict[str, Any],
) -> str:
    analysis_json_path = latest_run.get('ncu_analysis_path') or ncu_summary.get('analysis_path')
    analysis_md_path = sibling_repo_path(analysis_json_path, suffix='.md')
    human_guidance = ''
    if HUMAN_GUIDANCE_MD_PATH.exists():
        human_guidance = HUMAN_GUIDANCE_MD_PATH.read_text(encoding='utf-8').strip()
    human_guidance_block = human_guidance if human_guidance else '- no persistent human guidance recorded yet'
    cublas_baseline = benchmark_state.get('cublas_baseline') or {}
    cublas_ref_paths = [
        cublas_baseline.get('ncu_analysis_md'),
        cublas_baseline.get('ncu_analysis_json'),
        cublas_baseline.get('ncu_summary_json'),
        cublas_baseline.get('ncu_rep_path'),
    ]
    cublas_ref_paths = [path for path in cublas_ref_paths if path]
    autotune_paths = sorted(
        path for path in STATE_DIR.glob('autotune_*_main_tiles.*')
        if path.suffix in {'.json', '.md'}
    )
    autotune_lines = ''
    if autotune_paths:
        formatted = '\n'.join(f'- `{repo_rel(path)}`' for path in autotune_paths)
        autotune_lines = f'\n{formatted}\n'
    cublas_lines = '\n'.join(f'- `{path}`' for path in cublas_ref_paths) if cublas_ref_paths else '- no cuBLAS baseline artifacts are recorded yet'
    return textwrap.dedent(
        f'''\
        # Node B context

        Node B is the diagnosis node. Read the files below, then write exactly three directions to `state/latest_diagnosis.json`.
        Prioritize the structured bottleneck / hotspot / delta handoff first. Only fall back to raw CSV or `.ncu-rep` when the structured summary is insufficient.

        ## Read order

        - `state/node_b_context.md`
        - `state/latest_run.md`
        - `state/latest_ncu_summary.md`
        - `{analysis_md_path or 'N/A'}`
        - `{analysis_json_path or 'N/A'}`
        - `docs/heuristics.md`
        - `state/progress.md`
        - `state/current_focus.md`
        - `state/human_review.md`
        - `state/human_guidance.md`
        - `{graph_state.get('current_kernel_path', current_kernel_path())}`
        - `{latest_run.get('raw_summary_json', 'N/A')}`
        - `{ncu_summary.get('details_page_csv_path', 'N/A')}`
        - `{ncu_summary.get('source_csv_path', 'N/A')}`
        - `{ncu_summary.get('import_raw_csv_path', 'N/A')}`
        - `{ncu_summary.get('raw_details_csv_path', 'N/A')}`
        - `{ncu_summary.get('raw_csv_path', 'N/A')}`
        - `{ncu_summary.get('raw_rep_path', 'N/A')}`
{autotune_lines if autotune_lines else ''}

        ## Optional cuBLAS reference

        If the latest custom run does not suggest a clear next move, inspect the cuBLAS reference artifacts below to see how much hardware utilization the vendor library reaches on the same data.

{cublas_lines}

        Use the structured summary first:
        - `bottleneck_classes` tells you which bottleneck family is currently dominant
        - `top_findings` tells you which section, rule, hotspot, or delta is most actionable
        - `top_source_hotspots` and `handoff.node_c.target_hotspots` tell you where local hardware pressure concentrates
        - `delta_vs_previous_run` tells you what changed after the last code edit
        Use the raw exports only when the structured findings are not enough to explain pipeline, memory, synchronization, or source-level behavior.
        Use the autotune sweep summaries when present to anchor direction ranking in measured tile-width data instead of only one run snapshot.

        ## Persistent human guidance

        Review these items on every frontier-search / node_b ranking pass and map them explicitly into `family_audit`, diagnosis notes, or direction ranking when relevant.

{human_guidance_block}

        ## Output contract

        - write exactly 3 directions
        - preserve `direction_id` values `dir_01`, `dir_02`, `dir_03`
        - keep top-level `family_audit` as a list
        - keep top-level `selected_direction_id` as `null` during diagnosis emission unless a later explicit selection writes it
        - set `reasoning_source` to `main_llm_agent` or `llm_sub_agent` (legacy values `main_codex_agent` / `codex_sub_agent` are still accepted for backcompat)
        - set `reasoning_mode` to `manual_reasoned_best_model`
        - write a non-empty `reasoning_summary` with concrete ranking rationale
        - write `evidence_refs` as a non-empty list of concrete files reviewed
        - the diagnosis must come from live reasoning, not from a repo-external scripted helper
        - all 3 direction `name` fields must be distinct
        - all 3 direction `action_fingerprint` values must be distinct
        - each direction must include:
          - `family_id`
          - `subfamily_id`
          - `action_fingerprint`
          - `mode`
          - `hypothesis`
          - `expected_bottleneck`
          - `code_locations`
          - `risk`
          - `metrics_to_recheck`
          - `search_score_v1`
          - `score_breakdown`
          - `predicted_gain_ms`
          - `predicted_fail_risk`
          - `ranking_notes`
        - each direction may additionally include:
          - `evidence_refs`
          - `target_hotspots`
          - `expected_local_changes`
          - `guardrail_metrics`
        - set `recommended_direction_id`
        - every direction is also treated as a search candidate, so keep numeric score fields and prose notes auditable
        - after editing the diagnosis file, run `python scripts/graph.py node_b --finalize`

        ## Current source snapshot

        - round loop: `{round_label(round_loop)}`
        - rounds remaining after this one: `{max(round_loop.get('remaining_rounds', 0) - 1, 0) if round_loop.get('active') else 0}`
        - latest run id: `{latest_run.get('run_id', 'N/A')}`
        - median runtime: `{fmt_runtime(latest_run.get('median_runtime_ms'))}`
        - TFLOP/s: `{fmt_tflops(latest_run.get('tflops'))}`
        - measured commit: `{latest_run.get('measured_commit', 'N/A')}`
        - existing diagnosis status: `{diagnosis.get('status', 'pending_generation')}`
        - top bottleneck class: `{((ncu_summary.get('bottleneck_classes') or [{}])[0]).get('class_id', 'N/A')}`
        - top finding: `{((ncu_summary.get('top_findings') or [{}])[0]).get('summary', 'N/A')}`
        '''
    ).rstrip() + '\n'


def render_node_c_context(
    graph_state: Dict[str, Any],
    latest_run: Dict[str, Any],
    ncu_summary: Dict[str, Any],
    diagnosis: Dict[str, Any],
    active_direction: Dict[str, Any],
    dirty_paths: List[str],
    round_loop: Dict[str, Any],
) -> str:
    direction = active_direction_summary(active_direction, diagnosis)
    direction_name = direction.get('name') if direction else None
    direction_target_hotspots = normalize_dict_list(direction.get('target_hotspots'))
    target_hotspots = direction_target_hotspots or normalize_dict_list(
        ((ncu_summary.get('handoff') or {}).get('node_c') or {}).get('target_hotspots')
    )
    guardrail_metrics = normalize_dict_list(direction.get('guardrail_metrics')) or normalize_dict_list(
        ((ncu_summary.get('handoff') or {}).get('node_c') or {}).get('guardrail_metrics')
    )
    expected_local_changes = normalize_string_list(direction.get('expected_local_changes'))
    delta_summary = ncu_summary.get('delta_vs_previous_run') or {}
    hotspot_deltas = ncu_analysis.top_hotspot_deltas(delta_summary)
    recheck_points = normalize_dict_list(
        ((ncu_summary.get('handoff') or {}).get('node_c') or {}).get('expected_recheck_points')
    )
    relevant_bottlenecks = ncu_summary.get('bottleneck_classes') or []
    lines = ['# Node C context', '']
    lines.append('Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.')
    lines.append('Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.')
    lines.append('')
    lines.append('## Selected direction')
    lines.append('')
    lines.append(f"- direction id: `{active_direction.get('direction_id', 'N/A')}`")
    lines.append(f"- direction name: `{direction_name or active_direction.get('name') or 'N/A'}`")
    lines.append(f"- candidate id: `{active_direction.get('candidate_id', 'N/A')}`")
    lines.append(f"- base run id: `{active_direction.get('base_run_id', 'N/A')}`")
    lines.append(f"- primary family id: `{active_direction.get('family_id', direction.get('family_id') if direction else 'N/A')}`")
    lines.append(f"- planned action fingerprint: `{active_direction.get('action_fingerprint', direction.get('action_fingerprint') if direction else 'N/A')}`")
    lines.append(f"- selection mode: `{active_direction.get('selection_mode', 'N/A')}`")
    lines.append(f"- source diagnosis id: `{active_direction.get('source_diagnosis_id', 'N/A')}`")
    lines.append(f"- round loop: `{round_label(round_loop)}`")
    if direction:
        lines.append(f"- hypothesis: `{direction.get('hypothesis', 'N/A')}`")
        lines.append(f"- expected bottleneck: `{direction.get('expected_bottleneck', 'N/A')}`")
        lines.append(f"- code locations: `{', '.join(direction.get('code_locations', [])) or 'N/A'}`")
        lines.append(f"- risk: `{direction.get('risk', 'N/A')}`")
        lines.append(f"- metrics to re-check: `{', '.join(direction.get('metrics_to_recheck', [])) or 'N/A'}`")
    lines.append(f"- latest run id: `{latest_run.get('run_id', 'N/A')}`")
    lines.append(f"- latest runtime: `{fmt_runtime(latest_run.get('median_runtime_ms'))}`")
    lines.append(f"- latest NCU analysis: `{latest_run.get('ncu_analysis_path') or ncu_summary.get('analysis_path') or 'N/A'}`")
    lines.append('')
    lines.append('## Relevant hotspots')
    lines.append('')
    if target_hotspots:
        for item in target_hotspots[:6]:
            lines.append(f"- {format_hotspot_label(item)}")
    else:
        lines.append('- no structured hotspot list is available; fall back to `state/latest_ncu_summary.md` or raw exports only if needed')
    lines.append('')
    lines.append('## Relevant bottleneck evidence')
    lines.append('')
    if relevant_bottlenecks:
        for item in relevant_bottlenecks[:4]:
            lines.append(
                f"- `{item.get('class_id', 'unknown_bottleneck')}` | severity `{item.get('severity_score', 'N/A')}` | {item.get('summary', 'N/A')}"
            )
            for evidence in item.get('evidence', [])[:2]:
                lines.append(f"- evidence: {format_evidence_label(evidence)}")
    else:
        lines.append('- no structured bottleneck evidence is available')
    lines.append('')
    lines.append('## Guardrail metrics')
    lines.append('')
    if guardrail_metrics:
        for item in guardrail_metrics[:6]:
            lines.append(f"- {format_guardrail_label(item)}")
    else:
        lines.append('- no explicit guardrail metrics were provided')
    lines.append('')
    lines.append('## Expected local changes')
    lines.append('')
    if expected_local_changes:
        for item in expected_local_changes:
            lines.append(f"- `{item}`")
    else:
        lines.append('- no direction-specific local change notes were provided')
    lines.append('')
    lines.append('## Delta vs previous run')
    lines.append('')
    lines.append(f"- baseline run id: `{delta_summary.get('baseline_run_id', 'N/A')}`")
    stall_deltas = delta_summary.get('stall_breakdown') or []
    if stall_deltas:
        for item in stall_deltas[:4]:
            lines.append(
                f"- stall `{item.get('stall_group', 'unknown_stall')}` | delta `{item.get('delta', 'N/A')}` | trend `{item.get('trend', 'changed')}`"
            )
    else:
        lines.append('- no structured stall delta is available')
    if hotspot_deltas:
        for item in hotspot_deltas[:4]:
            lines.append(f"- hotspot delta: {format_delta_hotspot_label(item)}")
    else:
        lines.append('- no structured hotspot delta is available')
    lines.append('')
    lines.append('## Finalize recheck points')
    lines.append('')
    if recheck_points:
        for item in recheck_points[:6]:
            lines.append(
                f"- recheck `{item.get('scope_type', 'scope')}` `{item.get('scope_name', 'N/A')}` @ `{item.get('location', 'N/A')}` | `{item.get('metric_name', 'N/A')}` | {item.get('reason', 'N/A')}"
            )
    else:
        lines.append('- no explicit recheck points were provided')
    lines.append('')
    lines.append('## Allowed edit surface')
    lines.append('')
    lines.append('- `src/kernels/*`')
    lines.append('- `src/runner/main.cpp` when the direction requires runner glue')
    lines.append('- `include/*` when a stable interface change is required')
    lines.append('- `CMakeLists.txt` only if the build path genuinely needs it')
    lines.append('- `scripts/graph.py` or `scripts/sweep_fixed_main_tiles.py` only when the direction requires minimal workflow glue')
    lines.append('')
    lines.append('## Implementation notes')
    lines.append('')
    lines.append('- implement exactly one selected direction')
    lines.append('- stay within the primary family by default')
    lines.append('- if the implementation clearly crosses into another family, update `state/active_direction.json` and record `secondary_family_ids` before finalize')
    lines.append('- if the implementation semantically drifts from the planned action, update `implemented_action_fingerprint`, `semantic_delta_tags`, or `actual_code_regions` in `state/active_direction.json` before finalize')
    lines.append('- build failure is still recorded as a structured `state/latest_attempt.json` entry with `build_status=FAIL`')
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
        lines.append('- no active direction selected yet; use `python scripts/graph.py select-next` or `python scripts/graph.py use-recommended-direction` before using the dirty-path guardrail')
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
    search_frontier = load_search_frontier()
    normalize_search_frontier(search_frontier)
    reconcile_frontier_with_latest_attempt(search_frontier)
    refresh_frontier_family_representatives(search_frontier, load_search_state(), load_family_ledger())
    has_frontier_candidate = best_frontier_candidate(search_frontier, diagnosis) is not None
    task = {
        'supervisor_role': 'main_llm_agent',
        'dispatch_node': current_node,
        'dispatch_mode': 'direct_script',
        'graph_status': graph_state.get('status', 'unknown'),
        'round_label': round_label(round_loop),
        'round_loop_active': bool(round_loop.get('active')),
        'rounds_remaining': int(round_loop.get('remaining_rounds', 0)),
        'auto_use_recommended': bool(round_loop.get('auto_use_recommended')),
        'auto_select_frontier': bool(round_loop.get('auto_select_frontier')),
        'requires_gpu_access': False,
        'prepare_command': None,
        'selection_command': None,
        'finalize_command': None,
        'protocol_doc': 'docs/supervisor_protocol.md',
        'context_file': None,
        'active_direction_id': active_direction.get('direction_id'),
        'recommended_direction_id': diagnosis.get('recommended_direction_id'),
        'context_checkpoint_interval_rounds': context_compression_interval(),
        'last_context_checkpoint_round': latest_context_checkpoint_round(round_loop),
        'next_context_checkpoint_round': next_context_checkpoint_round(round_loop),
        'display_update_interval_rounds': display_update_interval(),
        'last_display_update_round': latest_display_update_round(round_loop),
        'next_display_update_round': next_display_update_round(round_loop),
        'display_update_due': display_update_due(round_loop),
        'display_update_instruction': (
            'Use the matmul-doc-sync skill or an equivalent narrow doc-refresh pass to update '
            '`README.md`, `blog/harness-engineering-human-in-the-loop-cuda-matmul/index.md`, '
            'and the rendered optimization tree, then commit only those doc/image files and run '
            '`git push origin HEAD`.'
        ),
        'watchdog_timeout_minutes': supervisor_watchdog_timeout_minutes(),
        'watchdog_status': 'idle',
        'watchdog_idle_minutes': None,
        'watchdog_latest_progress_at': None,
        'watchdog_latest_progress_path': None,
        'watchdog_continue_instruction': None,
        'continue_required': False,
        'natural_stop_disallowed': False,
        'stop_allowed': True,
        'stop_allowed_reasons': ['current_dispatch_complete', 'explicit_user_redirect'],
        'continue_until': None,
        'continue_instruction': None,
        'interrupt_policy': 'none',
        'notes': graph_state.get('notes', 'Inspect graph_state.json and dispatch the next node.'),
    }

    if current_node == 'node_a':
        task.update(
            {
                'dispatch_mode': 'direct_script',
                'requires_gpu_access': True,
                'prepare_command': 'python scripts/graph.py node_a',
                'protocol_doc': 'AGENTS.md',
                'notes': 'Run node_a directly from the main LLM agent outside the sandbox, then re-read graph state.',
            }
        )
    elif current_node == 'node_b':
        task.update(
            {
                'dispatch_mode': 'sub_agent',
                'prepare_command': 'python scripts/graph.py node_b',
                'finalize_command': 'python scripts/graph.py node_b --finalize',
                'protocol_doc': 'docs/node_b_protocol.md',
                'context_file': repo_rel(NODE_B_CONTEXT_PATH),
                'notes': 'Prepare node_b context if needed, spawn a diagnosis sub-agent for live reasoning, and do not replace node_b with a scripted helper before finalizing from the main LLM agent.',
            }
        )
    elif current_node == 'node_c':
        selection_command = None
        if not active_direction.get('direction_id'):
            if round_loop.get('active') and round_loop.get('auto_select_frontier') and has_frontier_candidate:
                selection_command = 'python scripts/graph.py select-next'
            elif diagnosis.get('recommended_direction_id') and (
                round_loop.get('auto_use_recommended') or round_loop.get('auto_select_frontier')
            ):
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
                'notes': 'Ensure exactly one direction is selected, spawn an implementation sub-agent for a real code edit, and do not replace node_c with a scripted helper before finalizing from the main LLM agent.',
            }
        )
    else:
        task['notes'] = f"Unknown current node {current_node!r}. Inspect state/graph_state.json before continuing."

    task.update(compute_watchdog_fields(task, graph_state, round_loop))
    task.update(compute_continue_contract_fields(task, round_loop))
    if task.get('continue_required'):
        task['notes'] = (
            f"{task.get('notes')} Active round loop in progress: `{graph_state.get('status', 'unknown')}` is a "
            'continue state, not a legal stop point. Re-read `state/supervisor_task.json` after every node and '
            'keep dispatching until `remaining_rounds = 0`, the graph fails/pauses, a required permission or '
            'environment dependency blocks execution, or the user explicitly redirects the conversation.'
        )
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
    lines.append('This file is for the main LLM supervisor. It decides whether to run the next step directly or dispatch a sub-agent.')
    lines.append('')
    lines.append('## Current dispatch')
    lines.append('')
    lines.append(f"- dispatch node: `{supervisor_task.get('dispatch_node', 'node_a')}`")
    lines.append(f"- dispatch mode: `{supervisor_task.get('dispatch_mode', 'direct_script')}`")
    lines.append(f"- graph status: `{supervisor_task.get('graph_status', 'unknown')}`")
    lines.append(f"- round label: `{supervisor_task.get('round_label', 'single-run')}`")
    lines.append(f"- round loop active: `{'yes' if supervisor_task.get('round_loop_active') else 'no'}`")
    lines.append(f"- rounds remaining: `{supervisor_task.get('rounds_remaining', 0)}`")
    lines.append(f"- auto-select frontier: `{'yes' if supervisor_task.get('auto_select_frontier') else 'no'}`")
    lines.append(f"- latest run id: `{latest_run.get('run_id', 'N/A')}`")
    lines.append(f"- latest runtime: `{fmt_runtime(latest_run.get('median_runtime_ms'))}`")
    lines.append(f"- recommended direction: `{diagnosis.get('recommended_direction_id', 'N/A')}`")
    lines.append(f"- active direction: `{active_direction.get('direction_id', 'N/A')}`")
    lines.append(f"- display update due at current checkpoint: `{'yes' if supervisor_task.get('display_update_due') else 'no'}`")
    lines.append(f"- watchdog status: `{supervisor_task.get('watchdog_status', 'idle')}`")
    lines.append(f"- continue required now: `{'yes' if supervisor_task.get('continue_required') else 'no'}`")
    lines.append(f"- stop allowed now: `{'yes' if supervisor_task.get('stop_allowed') else 'no'}`")
    lines.append(f"- natural stop states disallowed: `{'yes' if supervisor_task.get('natural_stop_disallowed') else 'no'}`")
    lines.append(f"- interrupt policy: `{supervisor_task.get('interrupt_policy', 'none')}`")
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
        lines.append(f"- auto-select frontier: `{'yes' if round_loop.get('auto_select_frontier') else 'no'}`")
        lines.append(f"- context compression cadence: every `{supervisor_task.get('context_checkpoint_interval_rounds', context_compression_interval())}` completed rounds")
        lines.append(f"- public display refresh cadence: every `{supervisor_task.get('display_update_interval_rounds', display_update_interval())}` completed rounds")
        if supervisor_task.get('last_context_checkpoint_round') is not None:
            lines.append(f"- last context compression checkpoint: after `{supervisor_task.get('last_context_checkpoint_round')}` completed rounds")
        if supervisor_task.get('next_context_checkpoint_round') is not None:
            lines.append(f"- next context compression checkpoint: after `{supervisor_task.get('next_context_checkpoint_round')}` completed rounds")
        if supervisor_task.get('last_display_update_round') is not None:
            lines.append(f"- last display refresh checkpoint: after `{supervisor_task.get('last_display_update_round')}` completed rounds")
        if supervisor_task.get('next_display_update_round') is not None:
            lines.append(f"- next display refresh checkpoint: after `{supervisor_task.get('next_display_update_round')}` completed rounds")
        lines.append(f"- display refresh checkpoint open now: `{'yes' if supervisor_task.get('display_update_due') else 'no'}`")
        lines.append(f"- display refresh action: {supervisor_task.get('display_update_instruction')}")
        lines.append(f"- continue until: `{supervisor_task.get('continue_until') or 'N/A'}`")
        if supervisor_task.get('continue_instruction'):
            lines.append(f"- immediate continue instruction: {supervisor_task.get('continue_instruction')}")
        lines.append(f"- allowed stop reasons while loop is active: `{', '.join(supervisor_task.get('stop_allowed_reasons') or [])}`")
        lines.append('- keep looping until `state/round_loop_state.json` reports `remaining_rounds = 0` or a failure pauses the loop')
    else:
        lines.append('- no multi-round loop is active')
        lines.append('- to arm one, run `python scripts/graph.py rounds --count N --auto-use-recommended`')
    lines.append('')
    lines.append('## Watchdog')
    lines.append('')
    lines.append(f"- timeout: `{supervisor_task.get('watchdog_timeout_minutes', supervisor_watchdog_timeout_minutes())}` minutes without workflow changes")
    lines.append(f"- latest observed progress: `{supervisor_task.get('watchdog_latest_progress_at') or 'N/A'}` via `{supervisor_task.get('watchdog_latest_progress_path') or 'N/A'}`")
    lines.append(f"- idle minutes: `{supervisor_task.get('watchdog_idle_minutes') if supervisor_task.get('watchdog_idle_minutes') is not None else 'N/A'}`")
    lines.append(f"- watchdog status: `{supervisor_task.get('watchdog_status', 'idle')}`")
    if supervisor_task.get('watchdog_continue_instruction'):
        lines.append(f"- continue instruction: {supervisor_task.get('watchdog_continue_instruction')}")
    else:
        lines.append('- continue instruction: `No watchdog action is currently required.`')
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
    search_state = load_search_state()
    round_loop = load_round_loop_state()
    write_text(LATEST_RUN_MD_PATH, render_latest_run_md(latest_run))
    write_text(LATEST_NCU_SUMMARY_MD_PATH, render_latest_ncu_md(latest_ncu))
    write_text(BENCHMARK_BASELINES_MD_PATH, render_benchmark_baselines_md(benchmark_state))
    write_text(ROUNDS_MD_PATH, render_rounds_md(round_loop))
    write_text(PROGRESS_MD_PATH, render_progress_md(graph_state, latest_run, diagnosis, active_direction, benchmark_state, search_state, round_loop))
    write_text(CURRENT_FOCUS_MD_PATH, render_current_focus_md(graph_state, latest_run, diagnosis, active_direction, search_state, round_loop))
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
            load_benchmark_state(),
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
            load_latest_run(),
            load_latest_ncu_summary(),
            load_latest_diagnosis(),
            load_active_direction(),
            dirty_paths,
            load_round_loop_state(),
        ),
    )


def start_round_loop(count: int, *, auto_use_recommended: bool, auto_select_frontier: bool) -> Dict[str, Any]:
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
            'auto_select_frontier': auto_select_frontier,
            'started_at': now_local_iso(),
            'completed_at': None,
            'last_completed_round': None,
            'accepted_base_run_id': latest_run.get('run_id'),
            'accepted_base_measured_commit': latest_run.get('measured_commit'),
            'accepted_base_runtime_ms': latest_run.get('median_runtime_ms'),
            'notes': (
                f'Started a {count}-round loop. '
                + (
                    'Frontier top candidates will auto-select, with fallback to the current recommended direction.'
                    if auto_select_frontier
                    else ('Recommended directions will auto-select.' if auto_use_recommended else 'Direction approval remains manual.')
                )
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
        'reasoning_source': diagnosis.get('reasoning_source'),
        'reasoning_mode': diagnosis.get('reasoning_mode'),
        'reasoning_summary': diagnosis.get('reasoning_summary'),
        'evidence_refs': diagnosis.get('evidence_refs', []),
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
        SEARCH_STATE_PATH,
        SEARCH_FRONTIER_PATH,
        SEARCH_CLOSED_PATH,
        FAMILY_LEDGER_PATH,
        SEARCH_CANDIDATES_PATH,
        LATEST_RUN_PATH,
        LATEST_RUN_MD_PATH,
        LATEST_NCU_SUMMARY_PATH,
        LATEST_NCU_SUMMARY_MD_PATH,
        LATEST_DIAGNOSIS_PATH,
        LATEST_ATTEMPT_PATH,
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
        HUMAN_GUIDANCE_MD_PATH,
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


def node_c_attempt_surface_paths() -> List[Path]:
    paths: List[Path] = [
        REPO_ROOT / 'src' / 'kernels',
        REPO_ROOT / 'src' / 'runner' / 'main.cpp',
        REPO_ROOT / 'include',
        REPO_ROOT / 'CMakeLists.txt',
        REPO_ROOT / 'scripts' / 'graph.py',
    ]
    if SWEEP_FIXED_MAIN_TILES_PATH.exists():
        paths.append(SWEEP_FIXED_MAIN_TILES_PATH)
    return paths


def supervisor_progress_watch_paths(graph_state: Dict[str, Any]) -> List[Path]:
    watched: List[Path] = [
        GRAPH_STATE_PATH,
        LATEST_RUN_PATH,
        LATEST_DIAGNOSIS_PATH,
        ACTIVE_DIRECTION_PATH,
        BENCHMARK_STATE_PATH,
        ROUND_LOOP_STATE_PATH,
        SEARCH_STATE_PATH,
        SEARCH_FRONTIER_PATH,
        SEARCH_CANDIDATES_PATH,
        FAMILY_LEDGER_PATH,
        LATEST_ATTEMPT_PATH,
    ]
    watched.extend(candidate_build_inputs())
    watched.append(REPO_ROOT / 'scripts' / 'graph.py')
    if SWEEP_FIXED_MAIN_TILES_PATH.exists():
        watched.append(SWEEP_FIXED_MAIN_TILES_PATH)

    current_kernel = graph_state.get('current_kernel_path')
    if current_kernel:
        watched.append(REPO_ROOT / current_kernel)
    return existing_files_in_scope(watched)


def iso_from_timestamp(timestamp: float) -> str:
    tz = dt.datetime.now().astimezone().tzinfo
    return dt.datetime.fromtimestamp(timestamp, tz=tz).isoformat(timespec='seconds')


def latest_progress_snapshot(graph_state: Dict[str, Any]) -> Dict[str, Any]:
    latest_path: Optional[Path] = None
    latest_mtime: Optional[float] = None
    for path in supervisor_progress_watch_paths(graph_state):
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        if latest_mtime is None or mtime > latest_mtime:
            latest_mtime = mtime
            latest_path = path
    return {
        'path': repo_rel(latest_path) if latest_path else None,
        'timestamp': iso_from_timestamp(latest_mtime) if latest_mtime is not None else None,
        'mtime': latest_mtime,
    }


def watchdog_continue_instruction(supervisor_task: Dict[str, Any], round_loop: Dict[str, Any]) -> Optional[str]:
    if not round_loop.get('active') or int(round_loop.get('remaining_rounds', 0) or 0) <= 0:
        return None
    dispatch_node = supervisor_task.get('dispatch_node')
    prepare = supervisor_task.get('prepare_command')
    finalize = supervisor_task.get('finalize_command')
    selection = supervisor_task.get('selection_command')
    if dispatch_node == 'node_a' and prepare:
        return f"Continue now by running `{prepare}` outside the sandbox, then re-read `state/supervisor_task.json`."
    if dispatch_node == 'node_b' and prepare and finalize:
        return (
            f"Continue now: run `{prepare}` if the node_b context is stale, spawn one diagnosis sub-agent "
            f"with `docs/node_b_protocol.md` + `state/node_b_context.md`, then run `{finalize}`."
        )
    if dispatch_node == 'node_c' and prepare and finalize:
        if selection:
            return (
                f"Continue now: run `{selection}` if no direction is selected, run `{prepare}`, spawn one "
                f"implementation sub-agent with `docs/node_c_protocol.md` + `state/node_c_context.md`, "
                f"then run `{finalize}`."
            )
        return (
            f"Continue now: run `{prepare}`, spawn one implementation sub-agent with "
            f"`docs/node_c_protocol.md` + `state/node_c_context.md`, then run `{finalize}`."
        )
    if prepare:
        return f"Continue now by dispatching the current step with `{prepare}` and then re-reading `state/supervisor_task.json`."
    return 'Continue now by re-reading `state/supervisor_task.json` and dispatching the current node.'


def compute_continue_contract_fields(
    supervisor_task: Dict[str, Any],
    round_loop: Dict[str, Any],
) -> Dict[str, Any]:
    active_loop = bool(round_loop.get('active')) and int(round_loop.get('remaining_rounds', 0) or 0) > 0
    fields: Dict[str, Any] = {
        'continue_required': False,
        'natural_stop_disallowed': False,
        'stop_allowed': True,
        'stop_allowed_reasons': ['current_dispatch_complete', 'explicit_user_redirect'],
        'continue_until': None,
        'continue_instruction': None,
        'interrupt_policy': 'none',
    }
    if not active_loop:
        return fields
    fields.update(
        {
            'continue_required': True,
            'natural_stop_disallowed': True,
            'stop_allowed': False,
            'stop_allowed_reasons': [
                'round_loop_complete',
                'graph_failure_or_pause',
                'permission_or_environment_block',
                'explicit_user_redirect',
            ],
            'continue_until': 'remaining_rounds == 0 or explicit_user_redirect',
            'continue_instruction': watchdog_continue_instruction(supervisor_task, round_loop),
            'interrupt_policy': 'only_explicit_user_redirect',
        }
    )
    return fields


def compute_watchdog_fields(
    supervisor_task: Dict[str, Any],
    graph_state: Dict[str, Any],
    round_loop: Dict[str, Any],
) -> Dict[str, Any]:
    timeout_minutes = supervisor_watchdog_timeout_minutes()
    snapshot = latest_progress_snapshot(graph_state)
    fields: Dict[str, Any] = {
        'watchdog_timeout_minutes': timeout_minutes,
        'watchdog_status': 'idle',
        'watchdog_idle_minutes': None,
        'watchdog_latest_progress_at': snapshot.get('timestamp'),
        'watchdog_latest_progress_path': snapshot.get('path'),
        'watchdog_continue_instruction': None,
    }
    if not round_loop.get('active') or int(round_loop.get('remaining_rounds', 0) or 0) <= 0:
        return fields

    fields['watchdog_status'] = 'healthy'
    latest_mtime = snapshot.get('mtime')
    if latest_mtime is None:
        fields['watchdog_status'] = 'stalled'
        fields['watchdog_continue_instruction'] = watchdog_continue_instruction(supervisor_task, round_loop)
        return fields

    idle_minutes = max((dt.datetime.now().astimezone().timestamp() - latest_mtime) / 60.0, 0.0)
    fields['watchdog_idle_minutes'] = round(idle_minutes, 1)
    if idle_minutes >= timeout_minutes:
        fields['watchdog_status'] = 'stalled'
        fields['watchdog_continue_instruction'] = watchdog_continue_instruction(supervisor_task, round_loop)
    return fields


def parse_numstat_output(text: str) -> Dict[str, int]:
    summary = {
        'files_changed': 0,
        'insertions': 0,
        'deletions': 0,
    }
    for line in text.splitlines():
        parts = line.split('\t', 2)
        if len(parts) != 3:
            continue
        added, deleted, _path = parts
        summary['files_changed'] += 1
        summary['insertions'] += int(added) if added.isdigit() else 0
        summary['deletions'] += int(deleted) if deleted.isdigit() else 0
    return summary


def diff_name_only_against_head(scope_paths: Sequence[Path | str]) -> List[str]:
    rels = relative_paths(scope_paths)
    proc = run_command(['git', 'diff', '--name-only', 'HEAD', '--', *rels], capture=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or 'failed to collect node_c changed paths')
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def diff_stats_against_head(scope_paths: Sequence[Path | str]) -> Dict[str, int]:
    rels = relative_paths(scope_paths)
    proc = run_command(['git', 'diff', '--numstat', 'HEAD', '--', *rels], capture=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or 'failed to collect node_c diff stats')
    return parse_numstat_output(proc.stdout)


def normalize_string_list(values: Any) -> List[str]:
    if not isinstance(values, list):
        return []
    return [str(value).strip() for value in values if str(value).strip()]


def is_compiled_node_c_path(rel_path: str) -> bool:
    return (
        rel_path.startswith('src/kernels/')
        or rel_path.startswith('include/')
        or rel_path == 'src/runner/main.cpp'
        or rel_path == 'CMakeLists.txt'
    )


def compiled_node_c_regions(actual_code_regions: Sequence[str]) -> List[str]:
    return [rel_path for rel_path in actual_code_regions if is_compiled_node_c_path(rel_path)]


def derive_semantic_delta_tags(actual_code_regions: Sequence[str], build_status: str) -> List[str]:
    tags: List[str] = ['single_direction_attempt']
    for rel_path in actual_code_regions:
        if rel_path.startswith('src/kernels/'):
            tags.append('kernel_code')
        elif rel_path == 'src/runner/main.cpp':
            tags.append('runner_glue')
        elif rel_path.startswith('include/'):
            tags.append('interface_glue')
        elif rel_path == 'CMakeLists.txt':
            tags.append('build_glue')
        elif rel_path.startswith('scripts/'):
            tags.append('workflow_glue')
    if build_status == 'FAIL':
        tags.append('build_failed')
    seen: set[str] = set()
    ordered: List[str] = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            ordered.append(tag)
    return ordered


def build_latest_attempt_payload(
    active_direction: Dict[str, Any],
    *,
    build_status: str,
    failure_mode: Optional[str],
    diff_stats: Dict[str, int],
    actual_code_regions: List[str],
    commit_sha: Optional[str] = None,
    commit_subject: Optional[str] = None,
) -> Dict[str, Any]:
    summary = active_direction.get('summary') or {}
    planned_action_fingerprint = active_direction.get('action_fingerprint') or summary.get('action_fingerprint')
    secondary_family_ids = normalize_string_list(active_direction.get('secondary_family_ids'))
    explicit_regions = normalize_string_list(active_direction.get('actual_code_regions'))
    if explicit_regions:
        actual_code_regions = explicit_regions
    semantic_delta_tags = normalize_string_list(active_direction.get('semantic_delta_tags'))
    if not semantic_delta_tags:
        semantic_delta_tags = derive_semantic_delta_tags(actual_code_regions, build_status)
    implemented_action_fingerprint = (
        active_direction.get('implemented_action_fingerprint')
        or planned_action_fingerprint
    )
    return {
        'schema_version': 1,
        'attempt_id': active_direction.get('candidate_id') or f"attempt_{timestamp_tag()}",
        'status': 'build_passed_pending_measurement' if build_status == 'PASS' else 'build_failed',
        'candidate_id': active_direction.get('candidate_id'),
        'source_diagnosis_id': active_direction.get('source_diagnosis_id'),
        'base_run_id': active_direction.get('base_run_id'),
        'family_id': active_direction.get('family_id') or summary.get('family_id'),
        'subfamily_id': active_direction.get('subfamily_id') or summary.get('subfamily_id'),
        'direction_id': active_direction.get('direction_id'),
        'direction_name': active_direction.get('name') or summary.get('name'),
        'mode': summary.get('mode'),
        'commit': commit_sha,
        'commit_short': commit_sha[:7] if commit_sha else None,
        'subject': commit_subject,
        'selection_mode': active_direction.get('selection_mode'),
        'selected_at': active_direction.get('selected_at'),
        'selected_from_frontier_id': active_direction.get('selected_from_frontier_id'),
        'source_run_id': active_direction.get('base_run_id'),
        'selection_score': active_direction.get('selection_priority'),
        'planned_action_fingerprint': planned_action_fingerprint,
        'implemented_action_fingerprint': implemented_action_fingerprint,
        'score_breakdown': summary.get('score_breakdown', {}),
        'semantic_delta_tags': semantic_delta_tags,
        'secondary_family_ids': secondary_family_ids,
        'actual_code_regions': actual_code_regions,
        'implementation': {
            'commit': commit_sha,
            'commit_short': commit_sha[:7] if commit_sha else None,
            'subject': commit_subject,
            'build_status': build_status,
            'failure_mode': failure_mode,
            'build_log_path': repo_rel(NODE_C_BUILD_LOG_PATH),
            'touched_files': actual_code_regions,
            'diff_stats': diff_stats,
        },
        'build_status': build_status,
        'failure_mode': failure_mode,
        'diff_stats': diff_stats,
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
        'transition_class': None,
        'close_reason': None,
        'notes': (
            'Build passed. Node A must measure this implementation next.'
            if build_status == 'PASS'
            else f'Build failed during node_c finalize with failure_mode={failure_mode}.'
        ),
    }


def commit_subject_from_message(message: str) -> Optional[str]:
    for line in message.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return None


def write_latest_attempt_payload(payload: Dict[str, Any]) -> None:
    write_json(LATEST_ATTEMPT_PATH, payload)
    search_state = load_search_state()
    search_state['latest_attempt_id'] = payload.get('attempt_id')
    search_state['active_candidate_id'] = payload.get('candidate_id')
    search_state['last_transition_type'] = 'node_c_finalize'
    search_state['notes'] = (
        f"Latest implementation edge recorded for {payload.get('candidate_id') or payload.get('direction_id') or 'unknown_candidate'}."
    )
    write_json(SEARCH_STATE_PATH, search_state)


def headline_metric_deltas(
    previous_metrics: Dict[str, Any],
    current_metrics: Dict[str, Any],
) -> Dict[str, float]:
    deltas: Dict[str, float] = {}
    for key, value in current_metrics.items():
        prev_value = previous_metrics.get(key)
        if isinstance(value, (int, float)) and isinstance(prev_value, (int, float)):
            deltas[key] = float(value) - float(prev_value)
    return deltas


def family_ledger_entry_defaults(family_id: str) -> Dict[str, Any]:
    return {
        'family_id': family_id,
        'wins': 0,
        'flats': 0,
        'losses': 0,
        'fails': 0,
        'last_transition_label': None,
        'freeze_status': 'open',
        'best_runtime_ms': None,
        'best_run_id': None,
        'last_result_run_id': None,
        'last_result_runtime_ms': None,
        'last_candidate_id': None,
        'last_attempt_id': None,
        'last_registers_per_thread': None,
        'last_shared_mem_per_block_allocated': None,
    }


def transition_bucket_from_label(transition_label: Optional[str]) -> Optional[str]:
    if transition_label == 'PASS_WIN':
        return 'wins'
    if transition_label == 'PASS_FLAT':
        return 'flats'
    if transition_label in ('PASS_LOSS', 'DIAG_POS_RUNTIME_NEG'):
        return 'losses'
    if transition_label in ('BUILD_FAIL', 'CORRECTNESS_FAIL'):
        return 'fails'
    return None


def freeze_status_from_transition_label(transition_label: Optional[str]) -> str:
    if transition_label == 'PASS_WIN':
        return 'open'
    if transition_label == 'PASS_FLAT':
        return 'frozen'
    if transition_label in ('PASS_LOSS', 'DIAG_POS_RUNTIME_NEG', 'BUILD_FAIL', 'CORRECTNESS_FAIL'):
        return 'closed_negative'
    return 'open'


def update_family_ledger_for_transition(
    family_ledger: Dict[str, Any],
    *,
    family_id: Optional[str],
    transition_label: Optional[str],
    candidate_id: Optional[str],
    attempt_id: Optional[str],
    result_run_id: Optional[str],
    result_runtime_ms: Optional[float],
    correctness_passed: Optional[bool],
    resource_snapshot: Dict[str, Any],
) -> None:
    if not family_id:
        return
    family_ledger['updated_at'] = now_local_iso()
    family_ledger['last_result_run_id'] = result_run_id
    family_ledger['last_transition_label'] = transition_label
    families = family_ledger.setdefault('families', {})
    family_entry = dict(family_ledger_entry_defaults(family_id))
    family_entry.update(families.get(family_id, {}))
    bucket = transition_bucket_from_label(transition_label)
    if bucket:
        family_entry[bucket] = int(family_entry.get(bucket, 0)) + 1
    family_entry['last_transition_label'] = transition_label
    family_entry['freeze_status'] = freeze_status_from_transition_label(transition_label)
    family_entry['last_result_run_id'] = result_run_id
    family_entry['last_result_runtime_ms'] = result_runtime_ms
    family_entry['last_candidate_id'] = candidate_id
    family_entry['last_attempt_id'] = attempt_id
    family_entry['last_registers_per_thread'] = resource_snapshot.get('registers_per_thread')
    family_entry['last_shared_mem_per_block_allocated'] = resource_snapshot.get('shared_mem_per_block_allocated')
    best_runtime_ms = family_entry.get('best_runtime_ms')
    if correctness_passed and result_runtime_ms is not None and (
        best_runtime_ms is None or float(result_runtime_ms) < float(best_runtime_ms)
    ):
        family_entry['best_runtime_ms'] = result_runtime_ms
        family_entry['best_run_id'] = result_run_id
    families[family_id] = family_entry


def attempt_matches_current_measurement(
    latest_attempt: Dict[str, Any],
    active_direction_before: Dict[str, Any],
) -> bool:
    if active_direction_before.get('status') != 'implemented_pending_measurement':
        return False
    if (latest_attempt.get('build_status') or '').upper() != 'PASS':
        return False
    attempt_candidate_id = latest_attempt.get('candidate_id')
    active_candidate_id = active_direction_before.get('candidate_id')
    if attempt_candidate_id and active_candidate_id:
        return attempt_candidate_id == active_candidate_id
    return latest_attempt.get('direction_id') == active_direction_before.get('direction_id')


def initialize_exact_base_if_missing(
    search_state: Dict[str, Any],
    previous_run: Dict[str, Any],
) -> None:
    if search_state.get('exact_base_run_id'):
        return
    seed_run_id = search_state.get('accepted_base_run_id') or previous_run.get('run_id')
    seed_runtime_ms = search_state.get('accepted_base_runtime_ms') or previous_run.get('median_runtime_ms')
    seed_commit = search_state.get('accepted_base_measured_commit') or previous_run.get('measured_commit')
    if seed_run_id:
        search_state['exact_base_run_id'] = seed_run_id
        search_state['exact_base_runtime_ms'] = seed_runtime_ms
        search_state['exact_base_measured_commit'] = seed_commit


def sync_best_known_run(search_state: Dict[str, Any], benchmark_state: Dict[str, Any]) -> None:
    best_known = benchmark_state.get('best_custom') or {}
    search_state['best_known_run_id'] = best_known.get('run_id')
    search_state['best_known_measured_commit'] = best_known.get('measured_commit')
    search_state['best_known_runtime_ms'] = best_known.get('median_runtime_ms')


def record_measurement_into_search_memory(
    previous_run: Dict[str, Any],
    previous_ncu: Dict[str, Any],
    latest_run: Dict[str, Any],
    latest_ncu: Dict[str, Any],
    benchmark_state: Dict[str, Any],
    active_direction_before: Dict[str, Any],
) -> None:
    latest_attempt = load_latest_attempt()
    matched_attempt = attempt_matches_current_measurement(latest_attempt, active_direction_before)
    resource_snapshot = {
        'registers_per_thread': latest_ncu.get('registers_per_thread'),
        'shared_mem_per_block_allocated': latest_ncu.get('shared_mem_per_block_allocated'),
    }
    search_state = load_search_state()
    initialize_exact_base_if_missing(search_state, previous_run)
    sync_best_known_run(search_state, benchmark_state)
    if not search_state.get('exact_base_run_id') and latest_run.get('run_id'):
        search_state['exact_base_run_id'] = latest_run.get('run_id')
        search_state['exact_base_measured_commit'] = latest_run.get('measured_commit')
        search_state['exact_base_runtime_ms'] = latest_run.get('median_runtime_ms')
    search_state['last_result_run_id'] = latest_run.get('run_id')
    search_state['last_result_measured_commit'] = latest_run.get('measured_commit')
    search_state['last_result_runtime_ms'] = latest_run.get('median_runtime_ms')
    search_state['last_result_correctness_passed'] = latest_run.get('correctness_passed')
    search_state['last_result_registers_per_thread'] = resource_snapshot['registers_per_thread']
    search_state['last_result_shared_mem_per_block_allocated'] = resource_snapshot['shared_mem_per_block_allocated']
    if not matched_attempt:
        search_state['status'] = 'measured_base_recorded'
        search_state['last_transition_type'] = 'node_a_measurement'
        search_state['notes'] = (
            f"Node A recorded measured run {latest_run.get('run_id')} without a matching active implementation attempt."
        )
        write_json(SEARCH_STATE_PATH, search_state)
        return

    direction_summary = active_direction_before.get('summary') or {}
    transition = classify_transition(
        previous_run.get('median_runtime_ms'),
        latest_run.get('median_runtime_ms'),
        latest_run.get('correctness_passed'),
        build_status=latest_attempt.get('build_status'),
        predicted_gain_ms=direction_summary.get('predicted_gain_ms'),
        enable_diag_pos_runtime_neg=False,
    )
    transition_label = transition.get('transition_label')
    runtime_delta_ms = transition.get('runtime_delta_ms')
    latest_attempt['status'] = 'measured'
    latest_attempt['measurement'] = {
        'run_id': latest_run.get('run_id'),
        'measurement_commit': latest_run.get('measured_commit'),
        'runtime_ms': latest_run.get('median_runtime_ms'),
        'runtime_delta_ms': runtime_delta_ms,
        'tflops': latest_run.get('tflops'),
        'correctness': latest_run.get('correctness_passed'),
        'ncu_analysis_path': latest_ncu.get('analysis_path'),
        'headline_metrics': latest_ncu.get('headline_metrics') or {},
        'headline_metric_deltas_vs_previous_run': headline_metric_deltas(
            previous_ncu.get('headline_metrics') or {},
            latest_ncu.get('headline_metrics') or {},
        ),
        'structured_bottleneck_deltas': list((latest_ncu.get('delta_vs_previous_run') or {}).get('stall_breakdown') or []),
        'top_hotspot_deltas': ncu_analysis.top_hotspot_deltas(latest_ncu.get('delta_vs_previous_run') or {}),
    }
    latest_attempt['transition_label'] = transition_label
    latest_attempt['transition_class'] = transition.get('transition_class')
    latest_attempt['close_reason'] = 'measured_by_node_a'
    latest_attempt['notes'] = (
        f"Node A measured {latest_run.get('run_id')} for candidate {latest_attempt.get('candidate_id') or latest_attempt.get('direction_id')}; "
        f"transition_label={transition_label}."
    )
    write_json(LATEST_ATTEMPT_PATH, latest_attempt)

    if transition_label == 'PASS_WIN':
        search_state['accepted_base_run_id'] = latest_run.get('run_id')
        search_state['accepted_base_measured_commit'] = latest_run.get('measured_commit')
        search_state['accepted_base_runtime_ms'] = latest_run.get('median_runtime_ms')
        search_state['exact_base_run_id'] = latest_run.get('run_id')
        search_state['exact_base_measured_commit'] = latest_run.get('measured_commit')
        search_state['exact_base_runtime_ms'] = latest_run.get('median_runtime_ms')
    search_state['status'] = 'measured_transition_recorded'
    search_state['active_candidate_id'] = None
    search_state['latest_attempt_id'] = latest_attempt.get('attempt_id')
    search_state['last_transition_type'] = 'node_a_measurement'
    search_state['last_transition_label'] = transition_label
    search_state['notes'] = (
        f"Node A recorded transition_label={transition_label} for candidate {latest_attempt.get('candidate_id') or latest_attempt.get('direction_id')}."
    )
    write_json(SEARCH_STATE_PATH, search_state)

    family_id = latest_attempt.get('family_id') or active_direction_before.get('family_id')
    family_ledger = load_family_ledger()
    update_family_ledger_for_transition(
        family_ledger,
        family_id=family_id,
        transition_label=transition_label,
        candidate_id=latest_attempt.get('candidate_id'),
        attempt_id=latest_attempt.get('attempt_id'),
        result_run_id=latest_run.get('run_id'),
        result_runtime_ms=latest_run.get('median_runtime_ms'),
        correctness_passed=latest_run.get('correctness_passed'),
        resource_snapshot=resource_snapshot,
    )
    if family_id:
        write_json(FAMILY_LEDGER_PATH, family_ledger)

    frontier = load_search_frontier()
    frontier_changed = normalize_search_frontier(frontier)
    frontier_changed = reconcile_frontier_with_latest_attempt(frontier) or frontier_changed
    frontier_changed = mark_frontier_candidate_closed(
        frontier,
        latest_attempt.get('candidate_id'),
        transition_label=transition_label,
        transition_class=transition.get('transition_class'),
        result_run_id=latest_run.get('run_id'),
        result_runtime_ms=latest_run.get('median_runtime_ms'),
        runtime_delta_ms=runtime_delta_ms,
        correctness_passed=latest_run.get('correctness_passed'),
        close_reason='measured_by_node_a',
        search_iteration=search_state.get('search_iteration'),
    ) or frontier_changed
    frontier_changed = refresh_frontier_family_representatives(frontier, search_state, family_ledger) or frontier_changed
    if frontier_changed:
        write_json(SEARCH_FRONTIER_PATH, frontier)

    append_jsonl(
        SEARCH_CLOSED_PATH,
        {
            'closed_at': now_local_iso(),
            'attempt_id': latest_attempt.get('attempt_id'),
            'candidate_id': latest_attempt.get('candidate_id'),
            'source_diagnosis_id': latest_attempt.get('source_diagnosis_id'),
            'base_run_id': latest_attempt.get('base_run_id'),
            'family_id': latest_attempt.get('family_id'),
            'subfamily_id': latest_attempt.get('subfamily_id'),
            'transition_label': transition_label,
            'transition_class': transition.get('transition_class'),
            'result_run_id': latest_run.get('run_id'),
            'result_runtime_ms': latest_run.get('median_runtime_ms'),
            'runtime_delta_ms': runtime_delta_ms,
            'correctness_passed': latest_run.get('correctness_passed'),
            'selection_score': latest_attempt.get('selection_score'),
            'planned_action_fingerprint': latest_attempt.get('planned_action_fingerprint'),
            'implemented_action_fingerprint': latest_attempt.get('implemented_action_fingerprint'),
            'registers_per_thread': resource_snapshot['registers_per_thread'],
            'shared_mem_per_block_allocated': resource_snapshot['shared_mem_per_block_allocated'],
            'close_reason': 'measured_by_node_a',
        },
    )


def record_build_failure_into_search_memory(
    latest_attempt: Dict[str, Any],
    active_direction: Dict[str, Any],
) -> None:
    if not latest_attempt.get('candidate_id'):
        return
    latest_attempt['status'] = 'closed'
    latest_attempt['transition_label'] = 'BUILD_FAIL'
    latest_attempt['transition_class'] = 'fail'
    latest_attempt['close_reason'] = 'build_failed_by_node_c'
    latest_attempt['notes'] = (
        f"Node C build failed for candidate {latest_attempt.get('candidate_id') or latest_attempt.get('direction_id')}; "
        'candidate closed as BUILD_FAIL.'
    )
    write_json(LATEST_ATTEMPT_PATH, latest_attempt)

    search_state = load_search_state()
    search_state['status'] = 'build_failed_recorded'
    search_state['active_candidate_id'] = None
    search_state['latest_attempt_id'] = latest_attempt.get('attempt_id')
    search_state['last_transition_type'] = 'node_c_build_failure'
    search_state['last_transition_label'] = 'BUILD_FAIL'
    search_state['notes'] = (
        f"Node C recorded BUILD_FAIL for candidate {latest_attempt.get('candidate_id') or latest_attempt.get('direction_id')}."
    )
    write_json(SEARCH_STATE_PATH, search_state)

    resource_snapshot = {
        'registers_per_thread': None,
        'shared_mem_per_block_allocated': None,
    }
    family_id = latest_attempt.get('family_id') or active_direction.get('family_id')
    if family_id:
        family_ledger = load_family_ledger()
        update_family_ledger_for_transition(
            family_ledger,
            family_id=family_id,
            transition_label='BUILD_FAIL',
            candidate_id=latest_attempt.get('candidate_id'),
            attempt_id=latest_attempt.get('attempt_id'),
            result_run_id=None,
            result_runtime_ms=None,
            correctness_passed=None,
            resource_snapshot=resource_snapshot,
        )
        write_json(FAMILY_LEDGER_PATH, family_ledger)
    else:
        family_ledger = load_family_ledger()

    frontier = load_search_frontier()
    frontier_changed = normalize_search_frontier(frontier)
    frontier_changed = reconcile_frontier_with_latest_attempt(frontier) or frontier_changed
    frontier_changed = mark_frontier_candidate_closed(
        frontier,
        latest_attempt.get('candidate_id'),
        transition_label='BUILD_FAIL',
        transition_class='fail',
        result_run_id=None,
        result_runtime_ms=None,
        runtime_delta_ms=None,
        correctness_passed=None,
        close_reason='build_failed_by_node_c',
        search_iteration=search_state.get('search_iteration'),
    ) or frontier_changed
    frontier_changed = refresh_frontier_family_representatives(frontier, search_state, family_ledger) or frontier_changed
    if frontier_changed:
        write_json(SEARCH_FRONTIER_PATH, frontier)

    append_jsonl(
        SEARCH_CLOSED_PATH,
        {
            'closed_at': now_local_iso(),
            'attempt_id': latest_attempt.get('attempt_id'),
            'candidate_id': latest_attempt.get('candidate_id'),
            'source_diagnosis_id': latest_attempt.get('source_diagnosis_id'),
            'base_run_id': latest_attempt.get('base_run_id'),
            'family_id': latest_attempt.get('family_id'),
            'subfamily_id': latest_attempt.get('subfamily_id'),
            'transition_label': 'BUILD_FAIL',
            'transition_class': 'fail',
            'result_run_id': None,
            'result_runtime_ms': None,
            'runtime_delta_ms': None,
            'correctness_passed': None,
            'selection_score': latest_attempt.get('selection_score'),
            'planned_action_fingerprint': latest_attempt.get('planned_action_fingerprint'),
            'implemented_action_fingerprint': latest_attempt.get('implemented_action_fingerprint'),
            'registers_per_thread': None,
            'shared_mem_per_block_allocated': None,
            'close_reason': 'build_failed_by_node_c',
        },
    )


def restore_result_summary(
    source_commit: str,
    *,
    changed_paths: Sequence[Path],
    commit_sha: Optional[str],
    reason: Optional[str],
) -> Dict[str, Any]:
    return {
        'source_commit': source_commit,
        'changed_paths': [repo_rel(path) or str(path) for path in changed_paths],
        'commit_sha': commit_sha,
        'reason': reason,
    }


def perform_restore_implementation(
    source_commit: str,
    *,
    reason: Optional[str],
    skip_commit: bool,
) -> Dict[str, Any]:
    # Restore only the compiled implementation surface. Keep workflow/workload
    # support files such as graph orchestration or sweep scripts on the current
    # HEAD so a historical family restore cannot silently downgrade the active
    # loop mode or the latest workload driver.
    tracked_non_state = [
        path for path in tracked_dirty_paths()
        if not path.startswith('state/')
    ]
    unrelated_dirty = [
        path for path in tracked_non_state
        if not path_is_allowed(path, RESTORE_IMPLEMENTATION_PATHS)
    ]
    if unrelated_dirty:
        raise RuntimeError(
            'refusing restore because unrelated tracked changes are present: '
            + ', '.join(unrelated_dirty)
        )

    changed_paths = restore_paths_from_commit(source_commit, RESTORE_IMPLEMENTATION_PATHS)
    refresh_node_c_context()

    if not changed_paths:
        print_step(f'implementation surface already matches {source_commit}')
        return restore_result_summary(
            source_commit,
            changed_paths=changed_paths,
            commit_sha=None,
            reason=reason,
        )

    commit_sha: Optional[str] = None
    if not skip_commit:
        commit_sha = commit_paths(
            changed_paths,
            infra_restore_commit_message(
                source_commit,
                reason or 're-measure or continue the next round from the restored baseline',
            ),
        )

    print_step(
        f'restored {len(changed_paths)} implementation path(s) from {source_commit}'
    )
    return restore_result_summary(
        source_commit,
        changed_paths=changed_paths,
        commit_sha=commit_sha,
        reason=reason,
    )


def resolve_run_id_to_restore_target(run_id: str) -> Dict[str, Any]:
    latest_run = load_latest_run()
    if latest_run.get('run_id') == run_id and latest_run.get('measured_commit'):
        return {
            'run_id': run_id,
            'source_commit': latest_run.get('measured_commit'),
            'runtime_ms': latest_run.get('median_runtime_ms'),
            'commit_field': 'measured_commit',
        }

    benchmark_state = load_benchmark_state()
    best_custom = benchmark_state.get('best_custom') or {}
    if best_custom.get('run_id') == run_id and best_custom.get('measured_commit'):
        return {
            'run_id': run_id,
            'source_commit': best_custom.get('measured_commit'),
            'runtime_ms': best_custom.get('median_runtime_ms'),
            'commit_field': 'measured_commit',
        }

    for entry in reversed(load_run_registry()):
        if entry.get('run_id') != run_id:
            continue
        source_commit = entry.get('measured_commit') or entry.get('source_commit')
        if source_commit:
            return {
                'run_id': run_id,
                'source_commit': source_commit,
                'runtime_ms': entry.get('median_runtime_ms'),
                'commit_field': 'measured_commit' if entry.get('measured_commit') else 'source_commit',
            }

    search_state = load_search_state()
    search_run_fields = (
        ('exact_base_run_id', 'exact_base_measured_commit', 'exact_base_runtime_ms'),
        ('accepted_base_run_id', 'accepted_base_measured_commit', 'accepted_base_runtime_ms'),
        ('best_known_run_id', 'best_known_measured_commit', 'best_known_runtime_ms'),
    )
    for run_field, commit_field, runtime_field in search_run_fields:
        if search_state.get(run_field) == run_id and search_state.get(commit_field):
            return {
                'run_id': run_id,
                'source_commit': search_state.get(commit_field),
                'runtime_ms': search_state.get(runtime_field),
                'commit_field': commit_field,
            }

    raise RuntimeError(f'could not resolve run_id {run_id} to a measured/source commit')


def record_restore_base_action(
    run_id: str,
    source_commit: str,
    runtime_ms: Optional[float],
    restore_result: Dict[str, Any],
) -> None:
    changed_files = list(restore_result.get('changed_paths', []))
    commit_sha = restore_result.get('commit_sha')
    commit_subject = (
        git_output(['show', '-s', '--format=%s', commit_sha])
        if commit_sha
        else None
    )
    diff_stats = {
        'files_changed': len(changed_files),
        'insertions': 0,
        'deletions': 0,
    }
    latest_attempt = {
        'schema_version': 1,
        'attempt_id': f'restore_base:{run_id}:{timestamp_tag()}',
        'status': 'restore_completed',
        'candidate_id': f'restore_base:{run_id}',
        'source_diagnosis_id': None,
        'base_run_id': run_id,
        'family_id': 'restore_base',
        'subfamily_id': 'restore_base.exact',
        'direction_id': 'restore_base',
        'direction_name': f'Restore implementation surface from {run_id}',
        'mode': 'restore',
        'commit': commit_sha,
        'commit_short': commit_sha[:7] if commit_sha else None,
        'subject': commit_subject,
        'selection_mode': 'restore',
        'selected_at': now_local_iso(),
        'selected_from_frontier_id': None,
        'source_run_id': run_id,
        'selection_score': None,
        'planned_action_fingerprint': f'restore_base:{source_commit}',
        'implemented_action_fingerprint': f'restore_base:{source_commit}',
        'score_breakdown': {},
        'semantic_delta_tags': ['restore_base'],
        'secondary_family_ids': [],
        'actual_code_regions': changed_files,
        'implementation': {
            'commit': commit_sha,
            'commit_short': commit_sha[:7] if commit_sha else None,
            'subject': commit_subject,
            'build_status': None,
            'failure_mode': None,
            'build_log_path': None,
            'touched_files': changed_files,
            'diff_stats': diff_stats,
        },
        'build_status': None,
        'failure_mode': None,
        'diff_stats': diff_stats,
        'measurement': {
            'run_id': None,
            'measurement_commit': source_commit,
            'runtime_ms': runtime_ms,
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
        'close_reason': 'restore_base',
        'notes': f'Restored implementation surface from run_id={run_id} using {source_commit}.',
    }
    write_json(LATEST_ATTEMPT_PATH, latest_attempt)

    search_state = load_search_state()
    search_state['status'] = 'restore_base_completed'
    search_state['exact_base_run_id'] = run_id
    search_state['exact_base_measured_commit'] = source_commit
    search_state['exact_base_runtime_ms'] = runtime_ms
    search_state['latest_attempt_id'] = latest_attempt.get('attempt_id')
    search_state['active_candidate_id'] = None
    search_state['last_transition_type'] = 'restore_base'
    search_state['last_restore_run_id'] = run_id
    search_state['last_restore_source_commit'] = source_commit
    search_state['last_restore_at'] = latest_attempt.get('selected_at')
    search_state['last_restore_reason'] = restore_result.get('reason')
    search_state['notes'] = f"Restored exact base from run_id={run_id} ({source_commit})."
    write_json(SEARCH_STATE_PATH, search_state)

    graph_state = load_graph_state()
    graph_state['notes'] = f"Restore-base reset the implementation surface to run_id={run_id}."
    write_json(GRAPH_STATE_PATH, graph_state)


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
    perform_restore_implementation(
        source_commit,
        reason=args.reason,
        skip_commit=args.skip_commit,
    )
    return 0


def run_restore_base(args: argparse.Namespace) -> int:
    ensure_machine_state()
    run_id = args.run_id.strip()
    if not run_id:
        raise RuntimeError('restore-base requires --run-id <run_id>')

    target = resolve_run_id_to_restore_target(run_id)
    restore_result = perform_restore_implementation(
        target['source_commit'],
        reason=args.reason or f'restore exact base from measured run {run_id}',
        skip_commit=True,
    )
    record_restore_base_action(
        run_id,
        target['source_commit'],
        target.get('runtime_ms'),
        restore_result,
    )
    refresh_all_views()
    if not args.skip_commit:
        commit_paths(
            node_state_paths_for_commit(restore_result.get('changed_paths', [])),
            infra_restore_commit_message(
                target['source_commit'],
                args.reason or f'restore exact base from measured run {run_id}',
            ),
        )
    print_step(
        f"restore-base resolved run_id={run_id} via {target.get('commit_field')}={target.get('source_commit')}"
    )
    return 0


def run_rebootstrap(args: argparse.Namespace) -> int:
    ensure_machine_state()
    baseline_run_id = args.baseline_run_id.strip()
    if not baseline_run_id:
        raise RuntimeError('rebootstrap requires --baseline-run-id <run_id>')

    target = resolve_run_id_to_restore_target(baseline_run_id)
    changed_paths = restore_paths_from_commit(target['source_commit'], REBOOTSTRAP_IMPLEMENTATION_PATHS)

    goal_summary = build_rebootstrap_goal_summary(
        goal_summary=args.goal_summary,
        goal_runtime_ms=args.goal_runtime_ms,
        goal_competitor=args.goal_competitor,
    )

    write_text(RUN_REGISTRY_PATH, '')
    write_text(ROUND_HISTORY_PATH, '')
    write_text(DIAGNOSIS_HISTORY_PATH, '')
    write_text(SEARCH_CLOSED_PATH, '')

    latest_run = default_latest_run()
    latest_ncu = default_latest_ncu_summary()
    diagnosis = default_latest_diagnosis()
    diagnosis['current_kernel_path'] = current_kernel_path()
    diagnosis['notes'] = (
        f"Branch rebootstrap restored implementation source from {baseline_run_id}. "
        'Run node_a first to capture a fresh branch-local baseline before node_b.'
    )
    active_direction = default_active_direction()
    active_direction['notes'] = (
        'No direction selected yet. The branch was rebootstrapped to a clean measurement-first state.'
    )

    round_loop = default_round_loop_state()
    round_loop.update(
        {
            'accepted_base_run_id': baseline_run_id,
            'accepted_base_measured_commit': target.get('source_commit'),
            'accepted_base_runtime_ms': target.get('runtime_ms'),
            'notes': (
                f"No multi-round loop is active. Historical restore anchor is {baseline_run_id}; "
                'run node_a to establish a fresh branch-local baseline before arming a new loop.'
            ),
        }
    )

    graph_state = default_graph_state()
    graph_state.update(
        {
            'current_node': 'node_a',
            'previous_node': None,
            'status': 'ready_for_node_a',
            'latest_run_dir': None,
            'latest_commit': None,
            'approved_direction_id': None,
            'recommended_direction_id': None,
            'current_kernel_path': current_kernel_path(),
            'plateau_counter': 0,
            'notes': (
                f"Implementation surface restored from historical baseline {baseline_run_id} "
                f"({target.get('source_commit')}). Run node_a to capture a fresh branch-local baseline."
            ),
        }
    )

    search_state = default_search_state()
    search_state.update(
        {
            'status': 'ready_for_branch_baseline',
            'goal_summary': goal_summary,
            'target_runtime_ms': parse_priority(args.goal_runtime_ms),
            'target_competitor': str(args.goal_competitor or '').strip() or None,
            'bootstrap_baseline_run_id': baseline_run_id,
            'bootstrap_baseline_measured_commit': target.get('source_commit'),
            'bootstrap_baseline_runtime_ms': target.get('runtime_ms'),
            'bootstrap_started_at': now_local_iso(),
            'accepted_base_run_id': baseline_run_id,
            'accepted_base_measured_commit': target.get('source_commit'),
            'accepted_base_runtime_ms': target.get('runtime_ms'),
            'best_known_run_id': baseline_run_id,
            'best_known_measured_commit': target.get('source_commit'),
            'best_known_runtime_ms': target.get('runtime_ms'),
            'exact_base_run_id': baseline_run_id,
            'exact_base_measured_commit': target.get('source_commit'),
            'exact_base_runtime_ms': target.get('runtime_ms'),
            'notes': (
                f"Branch rebootstrap complete from run_id={baseline_run_id}. "
                'The live search frontier/history was cleared; run node_a next.'
            ),
        }
    )

    benchmark_state = load_benchmark_state()
    benchmark_state['updated_at'] = now_local_iso()

    write_json(LATEST_RUN_PATH, latest_run)
    write_json(LATEST_NCU_SUMMARY_PATH, latest_ncu)
    write_json(LATEST_DIAGNOSIS_PATH, diagnosis)
    write_json(ACTIVE_DIRECTION_PATH, active_direction)
    write_json(GRAPH_STATE_PATH, graph_state)
    write_json(ROUND_LOOP_STATE_PATH, round_loop)
    write_json(SEARCH_STATE_PATH, search_state)
    write_json(SEARCH_FRONTIER_PATH, default_search_frontier())
    write_json(FAMILY_LEDGER_PATH, default_family_ledger())
    write_json(SEARCH_CANDIDATES_PATH, default_search_candidates())
    write_json(LATEST_ATTEMPT_PATH, default_latest_attempt())
    write_json(BENCHMARK_STATE_PATH, benchmark_state)

    refresh_all_views()
    print_step(
        f"rebootstrapped branch from {baseline_run_id} using {target.get('source_commit')}; "
        f"cleared live search history and restored {len(changed_paths)} implementation file(s)"
    )
    return 0


def run_node_a(args: argparse.Namespace) -> int:
    ensure_node_a_can_access_gpu()
    ensure_machine_state()
    graph_state = load_graph_state()
    previous_run = load_latest_run()
    previous_ncu = load_latest_ncu_summary()
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
    previous_analysis_path = resolve_repo_path(previous_ncu.get('analysis_path'))
    if previous_analysis_path and previous_analysis_path.exists():
        cmd.extend(['--previous-ncu-analysis', str(previous_analysis_path)])

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
    record_measurement_into_search_memory(
        previous_run,
        previous_ncu,
        latest_run,
        latest_ncu,
        benchmark_state,
        active_direction_before,
    )
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
    diagnosis['status'] = 'awaiting_llm'
    diagnosis['created_at'] = now_local_iso()
    diagnosis['source_run_id'] = latest_run.get('run_id')
    diagnosis['source_run_dir'] = latest_run.get('run_dir')
    diagnosis['source_summary_json'] = latest_run.get('raw_summary_json')
    diagnosis['source_ncu_summary_json'] = repo_rel(LATEST_NCU_SUMMARY_PATH)
    diagnosis['current_kernel_path'] = graph_state.get('current_kernel_path', current_kernel_path())
    diagnosis['reasoning_source'] = None
    diagnosis['reasoning_mode'] = None
    diagnosis['reasoning_summary'] = None
    diagnosis['evidence_refs'] = []
    diagnosis['selected_direction_id'] = None
    diagnosis['family_audit'] = []
    diagnosis['directions'] = [
        {
            'direction_id': 'dir_01',
            'rank': 1,
            'name': '',
            'family_id': '',
            'subfamily_id': '',
            'action_fingerprint': '',
            'mode': 'exploit',
            'hypothesis': '',
            'expected_bottleneck': '',
            'code_locations': [],
            'risk': '',
            'metrics_to_recheck': [],
            'search_score_v1': None,
            'score_breakdown': {},
            'predicted_gain_ms': None,
            'predicted_fail_risk': None,
            'ranking_notes': [],
            'stop_condition': '',
            'evidence_refs': [],
            'target_hotspots': [],
            'expected_local_changes': [],
            'guardrail_metrics': [],
        },
        {
            'direction_id': 'dir_02',
            'rank': 2,
            'name': '',
            'family_id': '',
            'subfamily_id': '',
            'action_fingerprint': '',
            'mode': 'exploit',
            'hypothesis': '',
            'expected_bottleneck': '',
            'code_locations': [],
            'risk': '',
            'metrics_to_recheck': [],
            'search_score_v1': None,
            'score_breakdown': {},
            'predicted_gain_ms': None,
            'predicted_fail_risk': None,
            'ranking_notes': [],
            'stop_condition': '',
            'evidence_refs': [],
            'target_hotspots': [],
            'expected_local_changes': [],
            'guardrail_metrics': [],
        },
        {
            'direction_id': 'dir_03',
            'rank': 3,
            'name': '',
            'family_id': '',
            'subfamily_id': '',
            'action_fingerprint': '',
            'mode': 'exploit',
            'hypothesis': '',
            'expected_bottleneck': '',
            'code_locations': [],
            'risk': '',
            'metrics_to_recheck': [],
            'search_score_v1': None,
            'score_breakdown': {},
            'predicted_gain_ms': None,
            'predicted_fail_risk': None,
            'ranking_notes': [],
            'stop_condition': '',
            'evidence_refs': [],
            'target_hotspots': [],
            'expected_local_changes': [],
            'guardrail_metrics': [],
        },
    ]
    return diagnosis


def score_breakdown_v1(rank: int, recommended: bool, risk_text: str | None) -> Dict[str, Any]:
    risk_level = normalize_risk_text_to_level(risk_text)
    risk_penalty = {
        0: 0.0,
        1: 0.4,
        2: 0.9,
        3: 1.2,
    }[risk_level]
    return {
        'policy_id': 'heuristic_v1_fallback',
        'rank_score': 4 - int(rank),
        'recommended_bonus': 0.25 if recommended else 0.0,
        'risk_level': risk_level,
        'risk_penalty': risk_penalty,
        'formula': 'rank_score + recommended_bonus - risk_penalty',
    }


def legacy_direction_slug(direction: Dict[str, Any]) -> str:
    seed = str(direction.get('name') or direction.get('direction_id') or 'legacy_direction').strip().lower()
    pieces: List[str] = []
    last_was_sep = False
    for char in seed:
        if char.isalnum():
            pieces.append(char)
            last_was_sep = False
            continue
        if not last_was_sep:
            pieces.append('_')
            last_was_sep = True
    slug = ''.join(pieces).strip('_')
    return slug or str(direction.get('direction_id') or 'legacy_direction')


def legacy_direction_mode(direction: Dict[str, Any]) -> str:
    name_text = str(direction.get('name') or '').lower()
    text = ' '.join(
        str(direction.get(key) or '').lower()
        for key in ('hypothesis', 'expected_bottleneck', 'stop_condition')
    )
    if any(keyword in name_text for keyword in ('restore base', 'rollback', 'revert', 'restore')):
        return 'restore'
    if any(keyword in name_text for keyword in ('retune', 'tune', 'tighten', 'trim', 'cadence', 'hot-band default', 're-lock', 'relock')):
        return 'exploit'
    if any(keyword in name_text for keyword in ('reopen', 'promote', 'explore', 'pivot', 'switch')):
        return 'explore'
    if any(keyword in text for keyword in ('rollback', 'revert', 'restore base')):
        return 'restore'
    return 'exploit'


def legacy_predicted_gain_ms(rank: int | None) -> float:
    return {
        1: 0.35,
        2: 0.2,
        3: 0.1,
    }.get(int(rank or 0), 0.05)


def legacy_predicted_fail_risk(risk_text: str | None) -> float:
    return {
        0: 0.15,
        1: 0.35,
        2: 0.6,
        3: 0.8,
    }[normalize_risk_text_to_level(risk_text)]


def legacy_ranking_notes(direction: Dict[str, Any], recommended: bool) -> List[str]:
    notes = direction.get('ranking_notes')
    if isinstance(notes, list):
        normalized = [str(note).strip() for note in notes if str(note).strip()]
    else:
        normalized = []
    if normalized:
        return normalized
    if recommended:
        return [
            'legacy diagnosis payload was backfilled into the search schema; keep the recommended direction as the deterministic fallback top candidate'
        ]
    return [
        'legacy diagnosis payload was backfilled into the search schema; keep this candidate as a lower-priority alternative until newer search-native scoring exists'
    ]


def canonical_accepted_base_anchor(
    search_state: Dict[str, Any],
    latest_run: Dict[str, Any],
) -> Dict[str, Any]:
    round_loop = load_round_loop_state()
    benchmark_state = load_benchmark_state()
    best_custom = benchmark_state.get('best_custom') or {}
    return {
        'run_id': (
            search_state.get('accepted_base_run_id')
            or round_loop.get('accepted_base_run_id')
            or best_custom.get('run_id')
            or latest_run.get('run_id')
        ),
        'measured_commit': (
            search_state.get('accepted_base_measured_commit')
            or round_loop.get('accepted_base_measured_commit')
            or best_custom.get('measured_commit')
            or latest_run.get('measured_commit')
        ),
        'runtime_ms': (
            search_state.get('accepted_base_runtime_ms')
            or round_loop.get('accepted_base_runtime_ms')
            or best_custom.get('median_runtime_ms')
            or latest_run.get('median_runtime_ms')
        ),
    }


def normalize_direction_for_finalize(direction: Dict[str, Any], recommended_direction_id: str | None) -> Dict[str, Any]:
    normalized = dict(direction)
    direction_id = normalized.get('direction_id')
    recommended = direction_id == recommended_direction_id
    slug = legacy_direction_slug(normalized)
    if not isinstance(normalized.get('name'), str) or not normalized.get('name', '').strip():
        normalized['name'] = str(direction_id or 'legacy_direction')
    if not isinstance(normalized.get('family_id'), str) or not normalized.get('family_id', '').strip():
        normalized['family_id'] = f'legacy::{slug}'
    if not isinstance(normalized.get('subfamily_id'), str) or not normalized.get('subfamily_id', '').strip():
        normalized['subfamily_id'] = normalized.get('family_id')
    if (
        normalized.get('mode') not in {'exploit', 'explore', 'restore'}
        or str(normalized.get('family_id') or '').startswith('legacy::')
    ):
        normalized['mode'] = legacy_direction_mode(normalized)
    for key in ('hypothesis', 'expected_bottleneck', 'risk', 'stop_condition'):
        if not isinstance(normalized.get(key), str) or not normalized.get(key, '').strip():
            normalized[key] = f'Legacy diagnosis backfill required for {direction_id} field={key}.'
    code_locations = normalized.get('code_locations')
    if not isinstance(code_locations, list):
        code_locations = []
    normalized['code_locations'] = [str(item).strip() for item in code_locations if str(item).strip()]
    if not normalized['code_locations']:
        normalized['code_locations'] = [current_kernel_path()]
    metrics = normalized.get('metrics_to_recheck')
    if not isinstance(metrics, list):
        metrics = []
    normalized['metrics_to_recheck'] = [str(item).strip() for item in metrics if str(item).strip()]
    if not normalized['metrics_to_recheck']:
        normalized['metrics_to_recheck'] = ['end-to-end median runtime']
    if not isinstance(normalized.get('action_fingerprint'), str) or not normalized.get('action_fingerprint', '').strip():
        normalized['action_fingerprint'] = make_action_fingerprint(normalized)
    if normalized.get('search_score_v1') is None:
        normalized['search_score_v1'] = fallback_search_score_v1(
            normalized.get('rank', 99),
            recommended,
            normalized.get('risk'),
        )
    if not isinstance(normalized.get('score_breakdown'), dict) or not normalized.get('score_breakdown'):
        normalized['score_breakdown'] = score_breakdown_v1(
            normalized.get('rank', 99),
            recommended,
            normalized.get('risk'),
        )
    if normalized.get('predicted_gain_ms') is None:
        normalized['predicted_gain_ms'] = legacy_predicted_gain_ms(normalized.get('rank'))
    if normalized.get('predicted_fail_risk') is None:
        normalized['predicted_fail_risk'] = legacy_predicted_fail_risk(normalized.get('risk'))
    normalized['ranking_notes'] = legacy_ranking_notes(normalized, recommended)
    normalized['evidence_refs'] = normalize_string_list(normalized.get('evidence_refs'))
    normalized['target_hotspots'] = normalize_dict_list(normalized.get('target_hotspots'))
    normalized['expected_local_changes'] = normalize_string_list(normalized.get('expected_local_changes'))
    normalized['guardrail_metrics'] = normalize_dict_list(normalized.get('guardrail_metrics'))
    return normalized


def normalize_diagnosis_for_finalize(diagnosis: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(diagnosis)
    if not isinstance(normalized.get('family_audit'), list):
        normalized['family_audit'] = []
    normalized['reasoning_source'] = (
        str(normalized.get('reasoning_source')).strip()
        if normalized.get('reasoning_source') is not None
        else None
    )
    normalized['reasoning_mode'] = (
        str(normalized.get('reasoning_mode')).strip()
        if normalized.get('reasoning_mode') is not None
        else None
    )
    normalized['reasoning_summary'] = (
        str(normalized.get('reasoning_summary')).strip()
        if normalized.get('reasoning_summary') is not None
        else None
    )
    normalized['evidence_refs'] = normalize_string_list(normalized.get('evidence_refs'))
    if not normalized.get('recommended_direction_id'):
        directions = normalized.get('directions', [])
        if directions:
            normalized['recommended_direction_id'] = directions[0].get('direction_id')
    normalized.setdefault('selected_direction_id', None)
    normalized['directions'] = [
        normalize_direction_for_finalize(direction, normalized.get('recommended_direction_id'))
        for direction in normalized.get('directions', [])
    ]
    return normalized


def _looks_like_placeholder(text: str) -> bool:
    lowered = text.strip().lower()
    placeholder_tokens = (
        'todo',
        'tbd',
        'placeholder',
        'auto-analysis',
        'auto analysis',
        'template',
        'fill me',
        'n/a',
        'unknown',
    )
    return any(token in lowered for token in placeholder_tokens)


def validate_diagnosis(
    diagnosis: Dict[str, Any],
    *,
    latest_run: Dict[str, Any],
    latest_ncu: Dict[str, Any],
) -> None:
    diagnosis_id = diagnosis.get('diagnosis_id')
    if not isinstance(diagnosis_id, str) or not diagnosis_id.strip():
        raise RuntimeError('node_b diagnosis requires a non-empty diagnosis_id')
    if diagnosis_id.startswith('auto_diagnosis_'):
        raise RuntimeError('node_b diagnosis ids must not be auto-generated helper ids')
    reasoning_source = diagnosis.get('reasoning_source')
    if reasoning_source not in {'main_codex_agent', 'codex_sub_agent', 'main_llm_agent', 'llm_sub_agent'}:
        raise RuntimeError('node_b diagnosis requires reasoning_source=main_llm_agent or llm_sub_agent (legacy main_codex_agent or codex_sub_agent also accepted)')
    reasoning_mode = diagnosis.get('reasoning_mode')
    if reasoning_mode != 'manual_reasoned_best_model':
        raise RuntimeError('node_b diagnosis requires reasoning_mode=manual_reasoned_best_model')
    reasoning_summary = diagnosis.get('reasoning_summary')
    if not isinstance(reasoning_summary, str) or len(reasoning_summary.strip()) < 80:
        raise RuntimeError('node_b diagnosis requires a non-trivial reasoning_summary')
    if _looks_like_placeholder(reasoning_summary):
        raise RuntimeError('node_b diagnosis reasoning_summary looks like placeholder text instead of live reasoning')
    source_run_id = diagnosis.get('source_run_id')
    if source_run_id != latest_run.get('run_id'):
        raise RuntimeError(
            f'node_b diagnosis must target the latest measured run ({latest_run.get("run_id")}); got {source_run_id}'
        )
    runtime_ms = latest_run.get('median_runtime_ms')
    if runtime_ms is not None:
        runtime_token = f'{float(runtime_ms):.3f}'
        if runtime_token not in reasoning_summary and str(latest_run.get('run_id')) not in reasoning_summary:
            raise RuntimeError(
                'node_b reasoning_summary must reference the live run context '
                '(include latest run id or current runtime).'
            )
    evidence_refs = set(normalize_string_list(diagnosis.get('evidence_refs')))
    required_evidence_refs = {
        'state/node_b_context.md',
        'state/latest_run.md',
        'state/latest_ncu_summary.md',
        'state/human_review.md',
    }
    missing_evidence_refs = sorted(required_evidence_refs.difference(evidence_refs))
    if missing_evidence_refs:
        raise RuntimeError(
            'node_b diagnosis is missing required evidence_refs: ' + ', '.join(missing_evidence_refs)
        )
    if not isinstance(diagnosis.get('family_audit'), list):
        raise RuntimeError('node_b diagnosis requires family_audit to be a list')
    if not diagnosis.get('family_audit'):
        raise RuntimeError('node_b diagnosis requires family_audit to document accept/defer/reject reasoning')
    directions = diagnosis.get('directions', [])
    if len(directions) != 3:
        raise RuntimeError('node_b requires exactly 3 directions')
    direction_names = {
        str(direction.get('name') or '').strip()
        for direction in directions
        if str(direction.get('name') or '').strip()
    }
    if len(direction_names) != 3:
        raise RuntimeError('node_b requires three distinct direction names')
    fingerprints = {
        str(direction.get('action_fingerprint') or '').strip()
        for direction in directions
        if str(direction.get('action_fingerprint') or '').strip()
    }
    if len(fingerprints) != 3:
        raise RuntimeError('node_b requires three distinct action_fingerprint values')
    ncu_metric_keys = set((latest_ncu.get('headline_metrics') or {}).keys())
    seen_ids = set()
    for direction in directions:
        direction_id = direction.get('direction_id')
        if not direction_id:
            raise RuntimeError('every direction needs a direction_id')
        if direction_id in seen_ids:
            raise RuntimeError(f'duplicate direction id: {direction_id}')
        seen_ids.add(direction_id)
        for key in (
            'name',
            'family_id',
            'subfamily_id',
            'mode',
            'hypothesis',
            'expected_bottleneck',
            'risk',
            'stop_condition',
        ):
            value = direction.get(key)
            if not isinstance(value, str) or not value.strip():
                raise RuntimeError(f'{direction_id} is missing non-empty field: {key}')
            if _looks_like_placeholder(value):
                raise RuntimeError(f'{direction_id} field {key} looks like placeholder text')
        if direction.get('mode') not in {'exploit', 'explore', 'restore'}:
            raise RuntimeError(f"{direction_id} mode must be one of: exploit, explore, restore")
        fingerprint = direction.get('action_fingerprint')
        if not isinstance(fingerprint, str) or not fingerprint.strip():
            raise RuntimeError(f'{direction_id} requires a non-empty action_fingerprint')
        code_locations = direction.get('code_locations')
        if not isinstance(code_locations, list) or not code_locations or not all(isinstance(item, str) and item.strip() for item in code_locations):
            raise RuntimeError(f'{direction_id} needs a non-empty code_locations list')
        metrics = direction.get('metrics_to_recheck')
        if not isinstance(metrics, list) or not metrics or not all(isinstance(item, str) and item.strip() for item in metrics):
            raise RuntimeError(f'{direction_id} needs a non-empty metrics_to_recheck list')
        if not any(metric in ncu_metric_keys for metric in metrics) and 'median runtime' not in ' '.join(metrics).lower():
            raise RuntimeError(
                f'{direction_id} metrics_to_recheck should include at least one live NCU headline metric '
                'or an explicit runtime metric'
            )
        if direction.get('search_score_v1') is None:
            raise RuntimeError(f'{direction_id} requires search_score_v1')
        try:
            float(direction.get('search_score_v1'))
        except (TypeError, ValueError) as exc:
            raise RuntimeError(f'{direction_id} search_score_v1 must be numeric') from exc
        score_breakdown = direction.get('score_breakdown')
        if not isinstance(score_breakdown, dict) or not score_breakdown:
            raise RuntimeError(f'{direction_id} requires a non-empty score_breakdown object')
        if direction.get('predicted_gain_ms') is None:
            raise RuntimeError(f'{direction_id} requires predicted_gain_ms')
        try:
            float(direction.get('predicted_gain_ms'))
        except (TypeError, ValueError) as exc:
            raise RuntimeError(f'{direction_id} predicted_gain_ms must be numeric') from exc
        if direction.get('predicted_fail_risk') is None:
            raise RuntimeError(f'{direction_id} requires predicted_fail_risk')
        try:
            float(direction.get('predicted_fail_risk'))
        except (TypeError, ValueError) as exc:
            raise RuntimeError(f'{direction_id} predicted_fail_risk must be numeric') from exc
        ranking_notes = direction.get('ranking_notes')
        if not isinstance(ranking_notes, list) or not all(isinstance(item, str) and item.strip() for item in ranking_notes):
            raise RuntimeError(f'{direction_id} requires ranking_notes as a non-empty string list')
        evidence_refs = direction.get('evidence_refs')
        if evidence_refs is not None and (
            not isinstance(evidence_refs, list)
            or not all(isinstance(item, str) and item.strip() for item in evidence_refs)
        ):
            raise RuntimeError(f'{direction_id} optional evidence_refs must be a string list when provided')
        expected_local_changes = direction.get('expected_local_changes')
        if expected_local_changes is not None and (
            not isinstance(expected_local_changes, list)
            or not all(isinstance(item, str) and item.strip() for item in expected_local_changes)
        ):
            raise RuntimeError(f'{direction_id} optional expected_local_changes must be a string list when provided')
        for key in ('target_hotspots', 'guardrail_metrics'):
            value = direction.get(key)
            if value is not None and (
                not isinstance(value, list)
                or not all(isinstance(item, dict) for item in value)
            ):
                raise RuntimeError(f'{direction_id} optional {key} must be a list of objects when provided')

    recommended = diagnosis.get('recommended_direction_id')
    if recommended not in seen_ids:
        raise RuntimeError('recommended_direction_id must reference one of the three directions')
    selected = diagnosis.get('selected_direction_id')
    if selected is not None and selected not in seen_ids:
        raise RuntimeError('selected_direction_id must be null or reference one of the three directions')


def diagnosis_candidate_id(diagnosis_id: str, direction_id: str) -> str:
    return f'{diagnosis_id}:{direction_id}'


def candidate_record_from_direction(
    diagnosis: Dict[str, Any],
    latest_run: Dict[str, Any],
    direction: Dict[str, Any],
) -> Dict[str, Any]:
    direction_id = direction.get('direction_id', 'dir_xx')
    candidate_id = diagnosis_candidate_id(diagnosis.get('diagnosis_id', 'diagnosis_unknown'), direction_id)
    recommended = direction_id == diagnosis.get('recommended_direction_id')
    return {
        'candidate_id': candidate_id,
        'source_diagnosis_id': diagnosis.get('diagnosis_id'),
        'base_run_id': latest_run.get('run_id'),
        'base_measured_commit': latest_run.get('measured_commit'),
        'base_runtime_ms': latest_run.get('median_runtime_ms'),
        'direction_id': direction_id,
        'direction_name': direction.get('name'),
        'family_id': direction.get('family_id'),
        'subfamily_id': direction.get('subfamily_id'),
        'action_fingerprint': direction.get('action_fingerprint'),
        'rank_in_diagnosis': direction.get('rank'),
        'recommended': recommended,
        'mode': direction.get('mode'),
        'priority': float(direction.get('search_score_v1')),
        'search_score_v1': float(direction.get('search_score_v1')),
        'score_breakdown': direction.get('score_breakdown'),
        'predicted_gain_ms': float(direction.get('predicted_gain_ms')),
        'predicted_fail_risk': float(direction.get('predicted_fail_risk')),
        'ranking_notes': direction.get('ranking_notes'),
        'hypothesis': direction.get('hypothesis'),
        'expected_bottleneck': direction.get('expected_bottleneck'),
        'code_locations': direction.get('code_locations'),
        'risk': direction.get('risk'),
        'metrics_to_recheck': direction.get('metrics_to_recheck'),
        'stop_condition': direction.get('stop_condition'),
        'evidence_refs': direction.get('evidence_refs'),
        'target_hotspots': direction.get('target_hotspots'),
        'expected_local_changes': direction.get('expected_local_changes'),
        'guardrail_metrics': direction.get('guardrail_metrics'),
        'status': 'open',
    }


def frontier_record_from_candidate(candidate: Dict[str, Any]) -> Dict[str, Any]:
    record = frontier_candidate_defaults(candidate.get('candidate_id'))
    record.update(copy.deepcopy(candidate))
    record['status'] = 'open'
    return normalize_frontier_candidate(record)


def merge_candidate_into_frontier(
    frontier: Dict[str, Any],
    candidate: Dict[str, Any],
    *,
    source_search_iteration: int,
) -> bool:
    existing = frontier_candidate_lookup(frontier, candidate.get('candidate_id'))
    if existing is None:
        record = frontier_record_from_candidate(candidate)
        record['source_search_iteration'] = source_search_iteration
        frontier.setdefault('candidates', []).append(normalize_frontier_candidate(record))
        return True

    raw = copy.deepcopy(existing)
    for key in (
        'source_diagnosis_id',
        'base_run_id',
        'base_measured_commit',
        'base_runtime_ms',
        'direction_id',
        'direction_name',
        'family_id',
        'subfamily_id',
        'action_fingerprint',
        'rank_in_diagnosis',
        'recommended',
        'mode',
        'priority',
        'search_score_v1',
        'score_breakdown',
        'predicted_gain_ms',
        'predicted_fail_risk',
        'ranking_notes',
        'hypothesis',
        'expected_bottleneck',
        'code_locations',
        'risk',
        'metrics_to_recheck',
        'stop_condition',
        'evidence_refs',
        'target_hotspots',
        'expected_local_changes',
        'guardrail_metrics',
    ):
        raw[key] = copy.deepcopy(candidate.get(key))
    if raw.get('source_search_iteration') is None:
        raw['source_search_iteration'] = source_search_iteration
    normalized = normalize_frontier_candidate(raw)
    if normalized != existing:
        existing.clear()
        existing.update(normalized)
        return True
    return False


def write_search_candidates_and_frontier(diagnosis: Dict[str, Any], latest_run: Dict[str, Any]) -> None:
    candidate_set_id = f"candidate_set:{diagnosis.get('diagnosis_id')}"
    candidates = [
        candidate_record_from_direction(diagnosis, latest_run, direction)
        for direction in diagnosis.get('directions', [])
    ]
    recommended_candidate = next(
        (candidate for candidate in candidates if candidate.get('direction_id') == diagnosis.get('recommended_direction_id')),
        None,
    )
    search_candidates = {
        'schema_version': 1,
        'candidate_set_id': candidate_set_id,
        'source_run_id': latest_run.get('run_id'),
        'source_diagnosis_id': diagnosis.get('diagnosis_id'),
        'generated_at': now_local_iso(),
        'recommended_direction_id': diagnosis.get('recommended_direction_id'),
        'recommended_candidate_id': recommended_candidate.get('candidate_id') if recommended_candidate else None,
        'candidates': candidates,
        'notes': 'Projected exactly three node_b directions into normalized search candidates.',
    }
    write_json(SEARCH_CANDIDATES_PATH, search_candidates)

    search_state = load_search_state()
    search_state['selection_policy'] = frontier_policy(search_state)
    next_search_iteration = int(search_state.get('search_iteration', 0)) + 1
    frontier = load_search_frontier()
    normalize_search_frontier(frontier)
    reconcile_frontier_with_latest_attempt(frontier)
    for candidate in candidates:
        merge_candidate_into_frontier(
            frontier,
            candidate,
            source_search_iteration=next_search_iteration,
        )
    frontier['schema_version'] = 2
    frontier['frontier_id'] = 'frontier:global'
    frontier['status'] = 'ready'
    frontier['source_run_id'] = latest_run.get('run_id')
    frontier['source_measured_commit'] = latest_run.get('measured_commit')
    frontier['source_diagnosis_id'] = diagnosis.get('diagnosis_id')
    frontier['candidate_set_id'] = candidate_set_id
    frontier['generated_at'] = frontier.get('generated_at') or now_local_iso()
    frontier['selection_policy_id'] = 'family_representative_v2'

    accepted_anchor = canonical_accepted_base_anchor(search_state, latest_run)
    search_state['search_iteration'] = next_search_iteration
    family_ledger = load_family_ledger()
    refresh_frontier_family_representatives(frontier, search_state, family_ledger)
    write_json(SEARCH_FRONTIER_PATH, frontier)

    search_state['status'] = 'frontier_ready'
    search_state['accepted_base_run_id'] = accepted_anchor.get('run_id')
    search_state['accepted_base_measured_commit'] = accepted_anchor.get('measured_commit')
    search_state['accepted_base_runtime_ms'] = accepted_anchor.get('runtime_ms')
    search_state['active_frontier_id'] = frontier.get('frontier_id')
    search_state['active_candidate_set_id'] = candidate_set_id
    search_state['active_candidate_id'] = None
    search_state['last_transition_type'] = 'candidate_emission'
    search_state['notes'] = (
        'Latest node_b finalize merged exactly three directions into the persistent frontier and refreshed one representative per family.'
    )
    write_json(SEARCH_STATE_PATH, search_state)


def run_node_b(args: argparse.Namespace) -> int:
    ensure_machine_state()
    latest_run = load_latest_run()
    if not latest_run.get('run_id'):
        raise RuntimeError('node_b requires a measured run first; run node_a')

    graph_state = load_graph_state()
    round_loop = load_round_loop_state()
    if args.finalize:
        latest_ncu = load_latest_ncu_summary()
        diagnosis = normalize_diagnosis_for_finalize(load_json_file(REPO_ROOT / args.diagnosis_file))
        validate_diagnosis(diagnosis, latest_run=latest_run, latest_ncu=latest_ncu)
        diagnosis['status'] = 'completed'
        diagnosis['created_at'] = diagnosis.get('created_at') or now_local_iso()
        diagnosis['source_run_id'] = diagnosis.get('source_run_id') or latest_run.get('run_id')
        diagnosis['source_run_dir'] = diagnosis.get('source_run_dir') or latest_run.get('run_dir')
        diagnosis['source_summary_json'] = diagnosis.get('source_summary_json') or latest_run.get('raw_summary_json')
        diagnosis['source_ncu_summary_json'] = diagnosis.get('source_ncu_summary_json') or repo_rel(LATEST_NCU_SUMMARY_PATH)
        diagnosis['current_kernel_path'] = diagnosis.get('current_kernel_path') or graph_state.get('current_kernel_path', current_kernel_path())
        diagnosis['selected_candidate_id'] = None
        write_json(LATEST_DIAGNOSIS_PATH, diagnosis)
        write_search_candidates_and_frontier(diagnosis, latest_run)

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
        if round_loop.get('active') and round_loop.get('auto_select_frontier'):
            try:
                select_next_candidate()
            except RuntimeError as exc:
                if str(exc) != 'no selectable frontier candidate is available':
                    raise
                recommended = diagnosis.get('recommended_direction_id')
                if recommended:
                    select_direction(recommended, 'recommended')
            round_loop = load_round_loop_state()
        elif round_loop.get('active') and round_loop.get('auto_use_recommended'):
            select_direction(diagnosis.get('recommended_direction_id'), 'recommended')
            round_loop = load_round_loop_state()
        refresh_all_views()
        if not args.skip_commit:
            commit_paths(node_state_paths_for_commit(), node_b_commit_message(diagnosis, latest_run, round_loop))
        if round_loop.get('active') and round_loop.get('auto_select_frontier'):
            print_step('node_b finalized; auto-selected the next frontier candidate for node_c')
        elif round_loop.get('active') and round_loop.get('auto_use_recommended'):
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


def select_candidate(candidate_id: str, selection_mode: str) -> int:
    ensure_machine_state()
    if not candidate_id:
        raise RuntimeError('candidate_id is required')
    frontier = load_search_frontier()
    normalize_search_frontier(frontier)
    reconcile_frontier_with_latest_attempt(frontier)
    refresh_frontier_family_representatives(frontier, load_search_state(), load_family_ledger())
    candidate = frontier_candidate_lookup(frontier, candidate_id)
    if candidate is None:
        raise RuntimeError(f'unknown candidate id: {candidate_id}')
    if candidate.get('status') in {'invalid', 'duplicate'}:
        raise RuntimeError(f'candidate {candidate_id} is not selectable; status={candidate.get("status")}')

    diagnosis = load_latest_diagnosis()
    summary = candidate_summary_from_record(candidate)
    active = {
        'direction_id': candidate.get('direction_id'),
        'name': candidate.get('direction_name') or summary.get('name'),
        'candidate_id': candidate.get('candidate_id'),
        'selected_from_frontier_id': frontier.get('frontier_id'),
        'family_id': candidate.get('family_id') or summary.get('family_id'),
        'subfamily_id': candidate.get('subfamily_id') or summary.get('subfamily_id'),
        'action_fingerprint': candidate.get('action_fingerprint') or summary.get('action_fingerprint'),
        'selection_priority': candidate.get('family_representative_score') or candidate.get('priority'),
        'base_run_id': candidate.get('base_run_id'),
        'selection_mode': selection_mode,
        'selected_at': now_local_iso(),
        'source_diagnosis_id': candidate.get('source_diagnosis_id'),
        'status': 'ready_for_implementation',
        'summary': summary,
        'notes': 'Node C may now implement this one candidate.',
    }
    write_json(ACTIVE_DIRECTION_PATH, active)

    if diagnosis.get('status') == 'completed':
        if selection_mode in ('approved', 'human_idea') and candidate.get('source_diagnosis_id') == diagnosis.get('diagnosis_id'):
            diagnosis['approved_direction_id'] = candidate.get('direction_id')
        diagnosis['selected_candidate_id'] = candidate.get('candidate_id')
        diagnosis['selected_direction_id'] = (
            candidate.get('direction_id')
            if candidate.get('source_diagnosis_id') == diagnosis.get('diagnosis_id')
            else None
        )
        write_json(LATEST_DIAGNOSIS_PATH, diagnosis)

    for other in frontier.get('candidates', []):
        if other.get('candidate_id') != candidate.get('candidate_id'):
            continue
        other['status'] = 'selected'
        other['selection_count'] = int(other.get('selection_count') or 0) + 1
        other['last_selected_at'] = active.get('selected_at')
        other['last_selected_selection_mode'] = selection_mode
    frontier['selected_candidate_id'] = candidate.get('candidate_id')
    frontier['selection_reason'] = (
        'frontier_top_family_representative'
        if selection_mode == 'frontier'
        else f'selected_via_{selection_mode}'
    )
    frontier['selection_summary'] = (
        f"Selected {candidate.get('candidate_id')} -> {candidate.get('direction_id')} via mode={selection_mode}."
    )
    write_json(SEARCH_FRONTIER_PATH, frontier)

    search_state = load_search_state()
    search_state['active_candidate_id'] = candidate.get('candidate_id')
    search_state['last_selected_candidate_id'] = candidate.get('candidate_id')
    search_state['last_selected_direction_id'] = candidate.get('direction_id')
    search_state['last_selected_selection_mode'] = selection_mode
    search_state['last_selected_at'] = active.get('selected_at')
    search_state['status'] = 'candidate_selected'
    search_state['notes'] = f"Selected frontier candidate {candidate.get('candidate_id')} for node_c."
    write_json(SEARCH_STATE_PATH, search_state)

    round_loop = mark_round_started_if_needed(load_round_loop_state())
    graph_state = load_graph_state()
    graph_state['current_node'] = 'node_c'
    graph_state['previous_node'] = 'node_b'
    graph_state['status'] = 'ready_for_node_c'
    graph_state['recommended_direction_id'] = diagnosis.get('recommended_direction_id')
    graph_state['approved_direction_id'] = diagnosis.get('approved_direction_id')
    if round_loop.get('active'):
        graph_state['notes'] = (
            f"Node C is ready to implement {candidate.get('candidate_id')} via {selection_mode} selection for {round_label(round_loop)}."
        )
    else:
        graph_state['notes'] = f"Node C is ready to implement {candidate.get('candidate_id')} via {selection_mode} selection."
    write_json(GRAPH_STATE_PATH, graph_state)
    refresh_all_views()
    print_step(f'selected {candidate.get("candidate_id")} for node_c using mode={selection_mode}')
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

    search_frontier = load_search_frontier()
    normalize_search_frontier(search_frontier)
    reconcile_frontier_with_latest_attempt(search_frontier)
    refresh_frontier_family_representatives(search_frontier, load_search_state(), load_family_ledger())
    matching_candidate = frontier_candidate_lookup(
        search_frontier,
        direction_id=direction_id,
        source_diagnosis_id=diagnosis.get('diagnosis_id'),
    )
    if matching_candidate is not None:
        return select_candidate(matching_candidate.get('candidate_id'), selection_mode)

    active = {
        'direction_id': direction_id,
        'name': direction.get('name'),
        'candidate_id': None,
        'selected_from_frontier_id': None,
        'family_id': direction.get('family_id'),
        'subfamily_id': direction.get('subfamily_id'),
        'action_fingerprint': direction.get('action_fingerprint'),
        'selection_priority': direction.get('search_score_v1'),
        'base_run_id': None,
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
    diagnosis['selected_direction_id'] = direction_id
    diagnosis['selected_candidate_id'] = None
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


def select_next_candidate() -> int:
    ensure_machine_state()
    active_direction = load_active_direction()
    if active_direction.get('direction_id'):
        raise RuntimeError('active_direction is already set; clear or finish the current selection before using select-next')

    diagnosis = load_latest_diagnosis()
    if diagnosis.get('status') != 'completed':
        raise RuntimeError('node_b must be finalized before selecting from the frontier')

    frontier = load_search_frontier()
    normalize_search_frontier(frontier)
    reconcile_frontier_with_latest_attempt(frontier)
    refresh_frontier_family_representatives(frontier, load_search_state(), load_family_ledger())
    candidates = frontier.get('candidates', [])
    if not candidates:
        raise RuntimeError('search frontier is empty; finalize node_b first')

    changed = False
    chosen: Optional[Dict[str, Any]] = None
    seen_fingerprints: set[str] = set()
    for candidate in selectable_frontier_candidates(frontier, diagnosis):
        reason = candidate_invalid_reason(candidate, diagnosis)
        fingerprint = str(candidate.get('action_fingerprint') or '').strip()
        if reason is not None:
            candidate['status'] = 'invalid'
            candidate['invalid_reason'] = reason
            changed = True
            continue
        if fingerprint in seen_fingerprints:
            continue
        chosen = candidate
        seen_fingerprints.add(fingerprint)
        break

    if chosen is None:
        if changed:
            write_json(SEARCH_FRONTIER_PATH, frontier)
        raise RuntimeError('no selectable frontier candidate is available')

    if changed:
        write_json(SEARCH_FRONTIER_PATH, frontier)
    return select_candidate(chosen.get('candidate_id'), 'frontier')


def run_search_status(_: argparse.Namespace) -> int:
    ensure_machine_state()
    search_state = load_search_state()
    frontier = load_search_frontier()
    normalize_search_frontier(frontier)
    reconcile_frontier_with_latest_attempt(frontier)
    refresh_frontier_family_representatives(frontier, search_state, load_family_ledger())
    diagnosis = load_latest_diagnosis()
    benchmark_state = load_benchmark_state()
    active_direction = load_active_direction()

    open_candidates = frontier_open_candidates(frontier)
    best_candidate = best_frontier_candidate(frontier, diagnosis)
    best_known = benchmark_state.get('best_custom') or {}

    print(f"search_status={search_state.get('status')}")
    print(f"frontier_id={frontier.get('frontier_id')}")
    print(f"frontier_open_count={len(open_candidates)}")
    print(f"family_representative_count={frontier.get('family_representative_count')}")
    print(f"best_candidate_id={best_candidate.get('candidate_id') if best_candidate else None}")
    print(f"best_candidate_direction_id={best_candidate.get('direction_id') if best_candidate else None}")
    print(
        f"best_candidate_priority={best_candidate.get('family_representative_score') if best_candidate else None}"
    )
    print(
        f"last_selected_candidate_id={search_state.get('last_selected_candidate_id') or active_direction.get('candidate_id')}"
    )
    print(
        f"last_selected_selection_mode={search_state.get('last_selected_selection_mode') or active_direction.get('selection_mode')}"
    )
    print(f"accepted_base_run_id={search_state.get('accepted_base_run_id')}")
    print(f"accepted_base_measured_commit={search_state.get('accepted_base_measured_commit')}")
    print(f"accepted_base_runtime_ms={search_state.get('accepted_base_runtime_ms')}")
    print(f"best_known_run_id={best_known.get('run_id')}")
    print(f"best_known_measured_commit={best_known.get('measured_commit')}")
    print(f"best_known_runtime_ms={best_known.get('median_runtime_ms')}")
    return 0


def run_frontier(args: argparse.Namespace) -> int:
    ensure_machine_state()
    frontier = load_search_frontier()
    normalize_search_frontier(frontier)
    reconcile_frontier_with_latest_attempt(frontier)
    refresh_frontier_family_representatives(frontier, load_search_state(), load_family_ledger())
    diagnosis = load_latest_diagnosis()
    candidates = frontier_open_candidates(frontier)
    print(f"frontier_id={frontier.get('frontier_id')}")
    print(f"status={frontier.get('status')}")
    print(f"open_count={len(candidates)}")
    print(f"family_representative_count={frontier.get('family_representative_count')}")
    print(f"selected_candidate_id={frontier.get('selected_candidate_id')}")
    limit = max(args.top, 0)
    for idx, candidate in enumerate(candidates[:limit], start=1):
        reason = candidate_invalid_reason(candidate, diagnosis)
        selectable = 'yes' if reason is None else 'no'
        print(
            f"{idx:02d} candidate_id={candidate.get('candidate_id')} "
            f"direction_id={candidate.get('direction_id')} "
            f"priority={candidate.get('family_representative_score') or candidate.get('priority')} "
            f"family_id={candidate.get('family_id')} "
            f"subfamily_id={candidate.get('subfamily_id')} "
            f"status={candidate.get('status')} "
            f"reopened={candidate.get('reopen_count')} "
            f"representative={'yes' if candidate.get('is_family_representative') else 'no'} "
            f"selectable={selectable}"
        )
    return 0


def run_select_next(_: argparse.Namespace) -> int:
    return select_next_candidate()


def run_node_c(args: argparse.Namespace) -> int:
    ensure_machine_state()
    graph_state = load_graph_state()
    diagnosis = load_latest_diagnosis()
    active_direction = load_active_direction()
    round_loop = load_round_loop_state()
    if not active_direction.get('direction_id'):
        raise RuntimeError('node_c requires an active direction; use select-next, approve, or use-recommended-direction first')

    direction = active_direction_summary(active_direction, diagnosis)
    if not direction:
        raise RuntimeError('active direction summary is missing; re-select a candidate before running node_c')

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

    attempt_scope_paths = node_c_attempt_surface_paths()
    commit_message = node_c_commit_message(active_direction, direction, round_loop)
    commit_subject = commit_subject_from_message(commit_message)
    actual_code_regions = diff_name_only_against_head(attempt_scope_paths)
    diff_stats = diff_stats_against_head(attempt_scope_paths)
    compiled_regions = compiled_node_c_regions(actual_code_regions)
    if not active_direction.get('actual_code_regions'):
        active_direction['actual_code_regions'] = actual_code_regions
    if not compiled_regions:
        latest_attempt = build_latest_attempt_payload(
            active_direction,
            build_status='FAIL',
            failure_mode='no_compiled_code_change',
            diff_stats=diff_stats,
            actual_code_regions=actual_code_regions,
            commit_sha=None,
            commit_subject=commit_subject,
        )
        write_latest_attempt_payload(latest_attempt)
        graph_state['current_node'] = 'node_c'
        graph_state['previous_node'] = 'node_b'
        graph_state['status'] = 'node_c_invalid_no_code_change'
        graph_state['notes'] = (
            'Node C finalize requires a real compiled-code edit in src/kernels/, include/, '
            'src/runner/main.cpp, or CMakeLists.txt before build.'
        )
        active_direction['status'] = 'invalid_no_code_change'
        active_direction['notes'] = graph_state['notes']
        write_json(GRAPH_STATE_PATH, graph_state)
        write_json(ACTIVE_DIRECTION_PATH, active_direction)
        record_build_failure_into_search_memory(latest_attempt, active_direction)
        if round_loop.get('active'):
            round_loop['status'] = 'paused_on_invalid_node_c'
            round_loop['notes'] = f'Paused {round_label(round_loop)} because node_c made no compiled code change.'
            write_json(ROUND_LOOP_STATE_PATH, round_loop)
        refresh_all_views()
        raise RuntimeError(
            'node_c finalize requires at least one compiled-code change before build '
            '(src/kernels/, include/, src/runner/main.cpp, or CMakeLists.txt)'
        )
    build_ok = maybe_run_build(runner_path, force=True, log_path=NODE_C_BUILD_LOG_PATH)
    if not active_direction.get('semantic_delta_tags'):
        active_direction['semantic_delta_tags'] = derive_semantic_delta_tags(
            actual_code_regions,
            'PASS' if build_ok else 'FAIL',
        )
    if not active_direction.get('implemented_action_fingerprint'):
        active_direction['implemented_action_fingerprint'] = active_direction.get('action_fingerprint')
    if not build_ok:
        latest_attempt = build_latest_attempt_payload(
            active_direction,
            build_status='FAIL',
            failure_mode='build_failed',
            diff_stats=diff_stats,
            actual_code_regions=actual_code_regions,
            commit_sha=None,
            commit_subject=commit_subject,
        )
        write_latest_attempt_payload(latest_attempt)
        graph_state['current_node'] = 'node_c'
        graph_state['previous_node'] = 'node_b'
        graph_state['status'] = 'node_c_build_failed'
        graph_state['notes'] = f'Build failed for {active_direction.get("direction_id")}; inspect {repo_rel(NODE_C_BUILD_LOG_PATH)}'
        active_direction['status'] = 'build_failed'
        active_direction['notes'] = f'Build failed; inspect {repo_rel(NODE_C_BUILD_LOG_PATH)}'
        write_json(GRAPH_STATE_PATH, graph_state)
        write_json(ACTIVE_DIRECTION_PATH, active_direction)
        record_build_failure_into_search_memory(latest_attempt, active_direction)
        if round_loop.get('active'):
            round_loop['status'] = 'paused_on_build_failure'
            round_loop['notes'] = f'Paused {round_label(round_loop)} because node_c failed to build.'
            write_json(ROUND_LOOP_STATE_PATH, round_loop)
        refresh_all_views()
        raise RuntimeError(f'node_c build failed; see {repo_rel(NODE_C_BUILD_LOG_PATH)}')

    active_direction['status'] = 'implemented_pending_measurement'
    active_direction['notes'] = 'Build passed. Node A must measure this implementation next.'
    write_json(ACTIVE_DIRECTION_PATH, active_direction)
    latest_attempt = build_latest_attempt_payload(
        active_direction,
        build_status='PASS',
        failure_mode=None,
        diff_stats=diff_stats,
        actual_code_regions=actual_code_regions,
        commit_sha=None,
        commit_subject=commit_subject,
    )
    write_latest_attempt_payload(latest_attempt)
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
    commit_sha: Optional[str] = None
    if not args.skip_commit:
        commit_sha = commit_paths(commit_list, commit_message)
        if commit_sha:
            latest_attempt = build_latest_attempt_payload(
                active_direction,
                build_status='PASS',
                failure_mode=None,
                diff_stats=diff_stats,
                actual_code_regions=actual_code_regions,
                commit_sha=commit_sha,
                commit_subject=git_output(['show', '-s', '--format=%s', commit_sha]),
            )
            write_latest_attempt_payload(latest_attempt)

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
    print(f"active_candidate_id={active_direction.get('candidate_id')}")
    print(f"round_loop_active={round_loop.get('active')}")
    print(f"round_loop_label={round_label(round_loop)}")
    print(f"rounds_remaining={round_loop.get('remaining_rounds')}")
    print(f"round_loop_status={round_loop.get('status')}")
    print(f"continue_required={supervisor_task.get('continue_required')}")
    print(f"stop_allowed={supervisor_task.get('stop_allowed')}")
    print(f"continue_until={supervisor_task.get('continue_until')}")
    print(f"continue_instruction={supervisor_task.get('continue_instruction')}")
    print(f"display_update_due={supervisor_task.get('display_update_due')}")
    print(f"watchdog_status={supervisor_task.get('watchdog_status')}")
    print(f"watchdog_idle_minutes={supervisor_task.get('watchdog_idle_minutes')}")
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
    print(f"continue_required={supervisor_task.get('continue_required')}")
    print(f"stop_allowed={supervisor_task.get('stop_allowed')}")
    print(f"continue_until={supervisor_task.get('continue_until')}")
    print(f"continue_instruction={supervisor_task.get('continue_instruction')}")
    print(f"interrupt_policy={supervisor_task.get('interrupt_policy')}")
    print(f"auto_select_frontier={supervisor_task.get('auto_select_frontier')}")
    print(f"context_checkpoint_interval_rounds={supervisor_task.get('context_checkpoint_interval_rounds')}")
    print(f"last_context_checkpoint_round={supervisor_task.get('last_context_checkpoint_round')}")
    print(f"next_context_checkpoint_round={supervisor_task.get('next_context_checkpoint_round')}")
    print(f"display_update_interval_rounds={supervisor_task.get('display_update_interval_rounds')}")
    print(f"last_display_update_round={supervisor_task.get('last_display_update_round')}")
    print(f"next_display_update_round={supervisor_task.get('next_display_update_round')}")
    print(f"display_update_due={supervisor_task.get('display_update_due')}")
    print(f"display_update_instruction={supervisor_task.get('display_update_instruction')}")
    print(f"watchdog_timeout_minutes={supervisor_task.get('watchdog_timeout_minutes')}")
    print(f"watchdog_status={supervisor_task.get('watchdog_status')}")
    print(f"watchdog_idle_minutes={supervisor_task.get('watchdog_idle_minutes')}")
    print(f"watchdog_latest_progress_at={supervisor_task.get('watchdog_latest_progress_at')}")
    print(f"watchdog_latest_progress_path={supervisor_task.get('watchdog_latest_progress_path')}")
    print(f"watchdog_continue_instruction={supervisor_task.get('watchdog_continue_instruction')}")
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
        print(f"auto_select_frontier={round_loop.get('auto_select_frontier')}")
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

    start_round_loop(
        args.count,
        auto_use_recommended=args.auto_use_recommended,
        auto_select_frontier=args.auto_select_frontier,
    )
    graph_state = load_graph_state()
    graph_state['notes'] = (
        f"Multi-round loop armed for {args.count} rounds. Continue with {graph_state.get('current_node', 'node_a')}."
    )
    write_json(GRAPH_STATE_PATH, graph_state)
    refresh_all_views()
    print_step(
        f"started a {args.count}-round loop"
        + (' with auto-select-frontier enabled' if args.auto_select_frontier else '')
        + (
            ' with auto-use-recommended enabled'
            if args.auto_use_recommended and not args.auto_select_frontier
            else ''
        )
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
        if not active_direction.get('direction_id') and round_loop.get('active'):
            if round_loop.get('auto_select_frontier'):
                try:
                    select_next_candidate()
                except RuntimeError as exc:
                    if str(exc) != 'no selectable frontier candidate is available':
                        raise
                    diagnosis = load_latest_diagnosis()
                    recommended = diagnosis.get('recommended_direction_id')
                    if recommended:
                        select_direction(recommended, 'recommended')
            elif round_loop.get('auto_use_recommended'):
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

    search_status = subparsers.add_parser('search-status', help='Print the current heuristic-search scaffold status')
    search_status.set_defaults(func=run_search_status)

    frontier = subparsers.add_parser('frontier', help='Inspect the current frontier')
    frontier.add_argument('--top', type=int, default=5)
    frontier.set_defaults(func=run_frontier)

    select_next = subparsers.add_parser('select-next', help='Select the highest-priority open frontier candidate for node_c')
    select_next.set_defaults(func=run_select_next)

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

    restore_base = subparsers.add_parser(
        'restore-base',
        help='Resolve a measured run_id to a restore commit, restore the implementation surface, and record it as a search action',
    )
    restore_base.add_argument('--run-id', required=True)
    restore_base.add_argument('--reason', default=None)
    restore_base.add_argument('--skip-commit', action='store_true')
    restore_base.set_defaults(func=run_restore_base)

    rebootstrap = subparsers.add_parser(
        'rebootstrap',
        help='Restore a measured implementation baseline and clear live workflow history for a fresh branch restart',
    )
    rebootstrap.add_argument('--baseline-run-id', required=True)
    rebootstrap.add_argument('--goal-runtime-ms', type=float, default=None)
    rebootstrap.add_argument('--goal-competitor', default=None)
    rebootstrap.add_argument('--goal-summary', default=None)
    rebootstrap.set_defaults(func=run_rebootstrap)

    status = subparsers.add_parser('status', help='Print the current graph state')
    status.set_defaults(func=run_status)

    rounds = subparsers.add_parser('rounds', help='Manage a multi-round node_b -> node_c -> node_a loop budget')
    rounds.add_argument('--count', type=int, default=None)
    rounds.add_argument('--auto-use-recommended', action='store_true')
    rounds.add_argument('--auto-select-frontier', action='store_true')
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
