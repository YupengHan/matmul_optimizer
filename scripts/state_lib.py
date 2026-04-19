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
SUPERVISOR_TASK_PATH = STATE_DIR / 'supervisor_task.json'


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
        'ncu_summary_json': repo_rel(LATEST_NCU_SUMMARY_PATH),
        'is_new_best_custom': False,
        'measured_commit': None,
        'generated_at': now_local_iso(),
    }


def default_latest_ncu_summary() -> Dict[str, Any]:
    return {
        'status': 'missing',
        'source_run_id': None,
        'source_run_dir': None,
        'kernel_name': None,
        'block_size': None,
        'grid_size': None,
        'registers_per_thread': None,
        'shared_mem_per_block_allocated': None,
        'headline_metrics': {},
        'raw_csv_path': None,
        'raw_rep_path': None,
        'generated_at': now_local_iso(),
    }


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
        'recommended_direction_id': None,
        'approved_direction_id': None,
        'directions': [],
        'notes': 'Run node_b to produce exactly three ranked directions.',
    }


def default_active_direction() -> Dict[str, Any]:
    return {
        'direction_id': None,
        'name': None,
        'selection_mode': None,
        'selected_at': None,
        'source_diagnosis_id': None,
        'status': 'idle',
        'summary': None,
        'notes': 'No direction selected yet. Use approve or use-recommended-direction after node_b.',
    }


def default_benchmark_state() -> Dict[str, Any]:
    return {
        'dataset_id': 'fixed_bf16_gemm_v1',
        'metric_of_record': 'median_runtime_ms',
        'cutlass_baseline': None,
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
        'supervisor_role': 'main_codex_agent',
        'dispatch_node': 'node_a',
        'dispatch_mode': 'direct_script',
        'graph_status': 'ready_for_node_a',
        'round_label': 'single-run',
        'round_loop_active': False,
        'rounds_remaining': 0,
        'auto_use_recommended': False,
        'requires_gpu_access': True,
        'prepare_command': 'python scripts/graph.py node_a',
        'selection_command': None,
        'finalize_command': None,
        'protocol_doc': 'AGENTS.md',
        'context_file': None,
        'active_direction_id': None,
        'recommended_direction_id': None,
        'notes': 'Run node_a directly from the main Codex agent.',
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


def load_graph_state() -> Dict[str, Any]:
    return load_json(GRAPH_STATE_PATH, default_graph_state())


def load_latest_run() -> Dict[str, Any]:
    return load_json(LATEST_RUN_PATH, default_latest_run())


def load_latest_ncu_summary() -> Dict[str, Any]:
    return load_json(LATEST_NCU_SUMMARY_PATH, default_latest_ncu_summary())


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
