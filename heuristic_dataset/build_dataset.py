#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from search_policy import classify_transition, fallback_search_score_v1, make_action_fingerprint, normalize_risk_text_to_level

SCHEMA_VERSION = 1

NODE_SUBJECT_RE = re.compile(r"^(node_[abc]): ")
NODE_A_SUBJECT_RE = re.compile(
    r"^node_a: (?P<round_label>.+?) measured (?P<run_id>\S+) for (?P<kernel_tag>\S+)$"
)
NODE_B_SUBJECT_RE = re.compile(
    r"^node_b: (?P<round_label>.+?) rank 3 directions from (?P<source_run_id>\S+)$"
)
NODE_C_SUBJECT_RE = re.compile(
    r"^node_c: (?P<round_label>.+?) implement (?P<direction_id>dir_\d+) (?P<direction_name>.+)$"
)
FLOAT_RE = re.compile(r"[-+]?\d+(?:\.\d+)?")


@dataclass
class CommitRecord:
    order: int
    sha: str
    subject: str
    body: str
    node_type: str

    @property
    def short(self) -> str:
        return self.sha[:7]


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def git_show_file(commit: str, path: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return None


def parse_json_text(text: str | None) -> dict[str, Any] | None:
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def load_json_at_commit(commit: str | None, path: str) -> dict[str, Any] | None:
    if not commit:
        return None
    return parse_json_text(git_show_file(commit, path))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=False) + "\n")


def maybe_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    match = FLOAT_RE.search(str(value))
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None


def first_non_null(*values: Any) -> Any:
    for value in values:
        if value is not None:
            return value
    return None


def parse_sections(body: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.endswith(":") and not line.startswith("- "):
            current = line[:-1]
            sections.setdefault(current, [])
            continue
        if line.startswith("- "):
            sections.setdefault(current or "_preamble", []).append(line[2:].strip())
    return sections


def parse_key_value_bullets(bullets: list[str]) -> tuple[dict[str, str], list[str]]:
    keyed: dict[str, str] = {}
    plain: list[str] = []
    for bullet in bullets:
        if ":" in bullet:
            key, value = bullet.split(":", 1)
            keyed[key.strip()] = value.strip()
        else:
            plain.append(bullet.strip())
    return keyed, plain


def parse_list_field(value: str | None) -> list[str]:
    if not value:
        return []
    parts = [part.strip() for part in value.split(",")]
    return [part for part in parts if part]


def parse_metric_direction(text: str | None) -> str | None:
    if not text:
        return None
    match = re.search(r"\(([^()]+)\)\s*$", text)
    if not match:
        return None
    return match.group(1).strip()


def normalize_metrics(raw_metrics: dict[str, Any] | None) -> dict[str, float]:
    if not raw_metrics:
        return {}
    normalized: dict[str, float] = {}
    for key, value in raw_metrics.items():
        numeric = maybe_float(value)
        if numeric is not None:
            normalized[key] = numeric
    return normalized


def compute_metric_deltas(
    current: dict[str, float], previous: dict[str, float]
) -> dict[str, float]:
    deltas: dict[str, float] = {}
    for key in sorted(set(current) & set(previous)):
        deltas[key] = round(current[key] - previous[key], 6)
    return deltas


def fallback_score_breakdown(
    rank: Any,
    recommended: bool,
    risk_text: str | None,
) -> dict[str, Any]:
    normalized_rank = int(rank) if rank is not None else None
    rank_score = (4 - normalized_rank) if normalized_rank is not None else None
    recommended_bonus = 0.25 if recommended else 0.0
    risk_level = normalize_risk_text_to_level(risk_text)
    risk_penalty = {
        0: 0.0,
        1: 0.4,
        2: 0.9,
        3: 1.2,
    }[risk_level]
    return {
        "policy_id": "heuristic_v1_fallback",
        "rank_score": rank_score,
        "recommended_bonus": recommended_bonus,
        "risk_level": risk_level,
        "risk_penalty": risk_penalty,
    }


def normalize_direction_record(
    direction: dict[str, Any],
    recommended_direction_id: str | None,
) -> dict[str, Any]:
    normalized = dict(direction)
    recommended = direction.get("direction_id") == recommended_direction_id
    fallback_breakdown = fallback_score_breakdown(
        direction.get("rank"),
        recommended,
        direction.get("risk"),
    )
    normalized.setdefault("family_id", None)
    normalized.setdefault("subfamily_id", None)
    normalized["action_fingerprint"] = (
        direction.get("action_fingerprint") or make_action_fingerprint(direction)
    )
    normalized.setdefault("mode", None)
    normalized["search_score_v1"] = first_non_null(
        direction.get("search_score_v1"),
        fallback_search_score_v1(
            int(direction.get("rank") or 0),
            recommended,
            direction.get("risk"),
        ) if direction.get("rank") is not None else None,
    )
    normalized["score_breakdown"] = direction.get("score_breakdown") or fallback_breakdown
    normalized.setdefault("predicted_gain_ms", None)
    normalized.setdefault("predicted_fail_risk", None)
    normalized["ranking_notes"] = direction.get("ranking_notes") or []
    return normalized


def correctness_to_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    text = str(value).strip().upper()
    if text == "PASS":
        return True
    if text == "FAIL":
        return False
    return None


def derive_semantic_delta_tags_from_files(touched_files: list[str]) -> list[str]:
    tags: list[str] = ["single_direction_attempt"]
    for path in touched_files:
        if path.startswith("src/kernels/"):
            tags.append("kernel_code")
        elif path == "src/runner/main.cpp":
            tags.append("runner_glue")
        elif path.startswith("include/"):
            tags.append("interface_glue")
        elif path == "CMakeLists.txt":
            tags.append("build_glue")
        elif path.startswith("scripts/"):
            tags.append("workflow_glue")
    seen: set[str] = set()
    ordered: list[str] = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            ordered.append(tag)
    return ordered


def derive_transition_label_from_measurement(
    parent_state_run_id: str | None,
    measurement: dict[str, Any] | None,
    build_status: str | None,
    predicted_gain_ms: float | None,
) -> str | None:
    if not measurement:
        return None
    previous_run = load_run_payload(parent_state_run_id)
    previous_runtime_ms = previous_run.get("runtime_ms")
    current_runtime_ms = measurement.get("runtime_ms")
    runtime_delta_ms = measurement.get("runtime_delta_ms")
    if (
        previous_runtime_ms is None
        and current_runtime_ms is not None
        and runtime_delta_ms is not None
    ):
        previous_runtime_ms = float(current_runtime_ms) - float(runtime_delta_ms)
    transition = classify_transition(
        previous_runtime_ms,
        current_runtime_ms,
        correctness_to_bool(measurement.get("correctness")),
        build_status=build_status,
        predicted_gain_ms=predicted_gain_ms,
        enable_diag_pos_runtime_neg=False,
    )
    return transition.get("transition_label")


def commit_parent(commit: str) -> str | None:
    line = git("rev-list", "--parents", "-n", "1", commit).strip().split()
    if len(line) < 2:
        return None
    return line[1]


def commit_touched_files(commit: str) -> list[str]:
    raw = git("diff-tree", "--root", "--no-commit-id", "--name-only", "-r", commit)
    return [line.strip() for line in raw.splitlines() if line.strip()]


def commit_diff_stats(commit: str) -> dict[str, Any]:
    raw = git("diff-tree", "--root", "--no-commit-id", "--numstat", "-r", commit)
    files_changed = 0
    insertions = 0
    deletions = 0
    code_files_changed = 0
    code_insertions = 0
    code_deletions = 0
    for line in raw.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        added_raw, deleted_raw, path = parts[0], parts[1], parts[2]
        files_changed += 1
        added = 0 if added_raw == "-" else int(added_raw)
        deleted = 0 if deleted_raw == "-" else int(deleted_raw)
        insertions += added
        deletions += deleted
        if not path.startswith("state/"):
            code_files_changed += 1
            code_insertions += added
            code_deletions += deleted
    return {
        "files_changed": files_changed,
        "insertions": insertions,
        "deletions": deletions,
        "code_files_changed": code_files_changed,
        "code_insertions": code_insertions,
        "code_deletions": code_deletions,
    }


def load_run_payload(run_id: str | None) -> dict[str, Any]:
    if not run_id:
        return {}
    run_dir = REPO_ROOT / "runs" / run_id
    summary = load_json(run_dir / "summary.json") or {}
    ncu_summary = load_json(run_dir / "ncu_summary.json") or {}
    perf_run = summary.get("perf_run") or {}
    runtime_ms = perf_run.get("runtime_ms") or {}
    headline_metrics = (
        summary.get("ncu", {}).get("headline_metrics")
        or ncu_summary.get("headline_metrics")
        or {}
    )
    return {
        "run_dir": f"runs/{run_id}",
        "summary_json_path": f"runs/{run_id}/summary.json",
        "ncu_summary_json_path": f"runs/{run_id}/ncu_summary.json",
        "ncu_rep_path": f"runs/{run_id}/ncu_profile.ncu-rep",
        "kernel_tag": summary.get("kernel_tag"),
        "runtime_ms": runtime_ms.get("median"),
        "runtime_p10_ms": runtime_ms.get("p10"),
        "runtime_p90_ms": runtime_ms.get("p90"),
        "tflops": perf_run.get("tflops"),
        "correctness_pass": all(
            run.get("passed") for run in summary.get("correctness_runs", [])
        )
        if summary.get("correctness_runs")
        else None,
        "registers_per_thread": ncu_summary.get("registers_per_thread"),
        "shared_mem_per_block_allocated": ncu_summary.get(
            "shared_mem_per_block_allocated"
        ),
        "resource_snapshot": {
            "registers_per_thread": ncu_summary.get("registers_per_thread"),
            "shared_mem_per_block_allocated": ncu_summary.get(
                "shared_mem_per_block_allocated"
            ),
        },
        "headline_metrics": normalize_metrics(headline_metrics),
        "raw_summary": summary,
        "raw_ncu_summary": ncu_summary,
    }


def collect_commit_stream(head_commit: str) -> list[CommitRecord]:
    raw = git(
        "log",
        "--reverse",
        head_commit,
        "--extended-regexp",
        "--grep",
        r"^node_[abc]:",
        "--format=%H%x1f%s%x1f%b%x1e",
    )
    records: list[CommitRecord] = []
    for order, chunk in enumerate(record for record in raw.split("\x1e") if record.strip()):
        sha, subject, body = chunk.split("\x1f", 2)
        subject = subject.strip()
        match = NODE_SUBJECT_RE.match(subject)
        if not match:
            continue
        records.append(
            CommitRecord(
                order=order,
                sha=sha.strip(),
                subject=subject,
                body=body.strip(),
                node_type=match.group(1),
            )
        )
    return records


def build_node_a_map(node_a_records: list[CommitRecord]) -> dict[str, dict[str, Any]]:
    measurements_by_short: dict[str, dict[str, Any]] = {}
    for record in node_a_records:
        match = NODE_A_SUBJECT_RE.match(record.subject)
        if not match:
            continue
        subject_meta = match.groupdict()
        sections = parse_sections(record.body)
        measurement_kv, _ = parse_key_value_bullets(sections.get("Measurement", []))
        run_id = subject_meta["run_id"]
        previous_run_id = measurement_kv.get("previous run id")
        run_payload = load_run_payload(run_id)
        previous_payload = load_run_payload(previous_run_id)
        current_metrics = run_payload.get("headline_metrics") or {}
        previous_metrics = previous_payload.get("headline_metrics") or {}
        measurements_by_short[subject_meta["kernel_tag"].rsplit("_", 1)[-1]] = {
            "schema_version": SCHEMA_VERSION,
            "measurement_commit": record.sha,
            "measurement_commit_short": record.short,
            "measurement_subject": record.subject,
            "measurement_order": record.order,
            "round_label": subject_meta["round_label"],
            "run_id": run_id,
            "kernel_tag": subject_meta["kernel_tag"],
            "previous_run_id": previous_run_id,
            "run_dir": measurement_kv.get("run dir") or run_payload.get("run_dir"),
            "summary_json_path": run_payload.get("summary_json_path"),
            "ncu_summary_json_path": run_payload.get("ncu_summary_json_path"),
            "ncu_rep_path": measurement_kv.get("ncu rep path")
            or run_payload.get("ncu_rep_path"),
            "runtime_ms": run_payload.get("runtime_ms")
            or maybe_float(measurement_kv.get("median runtime")),
            "runtime_p10_ms": run_payload.get("runtime_p10_ms"),
            "runtime_p90_ms": run_payload.get("runtime_p90_ms"),
            "runtime_delta_ms": maybe_float(
                measurement_kv.get("runtime delta vs previous measured run")
            ),
            "runtime_delta_label": parse_metric_direction(
                measurement_kv.get("runtime delta vs previous measured run")
            ),
            "tflops": run_payload.get("tflops")
            or maybe_float(measurement_kv.get("TFLOP/s")),
            "tflops_delta": maybe_float(
                measurement_kv.get("TFLOP/s delta vs previous measured run")
            ),
            "correctness": measurement_kv.get("correctness")
            or ("PASS" if run_payload.get("correctness_pass") else None),
            "tensor_pipe_active": maybe_float(measurement_kv.get("tensor pipe active")),
            "resource_snapshot": run_payload.get("resource_snapshot") or {},
            "headline_metrics": current_metrics,
            "headline_metric_deltas_vs_previous_run": compute_metric_deltas(
                current_metrics, previous_metrics
            ),
        }
    return measurements_by_short


def build_diagnosis_records(
    diagnosis_commits: list[CommitRecord],
    node_c_commits: list[CommitRecord],
) -> list[dict[str, Any]]:
    diagnosis_records: list[dict[str, Any]] = []
    node_c_by_order = sorted(node_c_commits, key=lambda record: record.order)
    diagnosis_orders = [record.order for record in diagnosis_commits]
    for index, record in enumerate(diagnosis_commits):
        match = NODE_B_SUBJECT_RE.match(record.subject)
        if not match:
            continue
        subject_meta = match.groupdict()
        diagnosis_text = git_show_file(record.sha, "state/latest_diagnosis.json")
        diagnosis_payload = parse_json_text(diagnosis_text) or {}
        next_diagnosis_order = diagnosis_orders[index + 1] if index + 1 < len(diagnosis_orders) else None
        selected_node_c = None
        for candidate in node_c_by_order:
            if candidate.order <= record.order:
                continue
            if next_diagnosis_order is not None and candidate.order >= next_diagnosis_order:
                break
            selected_node_c = candidate
            break
        selected_direction_id = None
        selected_direction_name = None
        selected_commit = None
        if selected_node_c:
            node_c_match = NODE_C_SUBJECT_RE.match(selected_node_c.subject)
            if node_c_match:
                selected_direction_id = node_c_match.group("direction_id")
                selected_direction_name = node_c_match.group("direction_name")
                selected_commit = selected_node_c.sha
        run_payload = load_run_payload(subject_meta["source_run_id"])
        normalized_directions = [
            normalize_direction_record(
                direction,
                diagnosis_payload.get("recommended_direction_id"),
            )
            for direction in diagnosis_payload.get("directions", [])
        ]
        payload_selected_direction_id = diagnosis_payload.get("selected_direction_id")
        payload_selected_direction_name = next(
            (
                direction.get("name")
                for direction in normalized_directions
                if direction.get("direction_id") == payload_selected_direction_id
            ),
            None,
        )
        diagnosis_records.append(
            {
                "schema_version": SCHEMA_VERSION,
                "diagnosis_commit": record.sha,
                "diagnosis_commit_short": record.short,
                "diagnosis_subject": record.subject,
                "round_label": subject_meta["round_label"],
                "diagnosis_id": diagnosis_payload.get("diagnosis_id"),
                "status": diagnosis_payload.get("status"),
                "created_at": diagnosis_payload.get("created_at"),
                "source_run_id": diagnosis_payload.get("source_run_id")
                or subject_meta["source_run_id"],
                "source_run_dir": diagnosis_payload.get("source_run_dir"),
                "source_summary_json": diagnosis_payload.get("source_summary_json"),
                "source_ncu_summary_json": diagnosis_payload.get("source_ncu_summary_json"),
                "heuristics_path": diagnosis_payload.get("heuristics_path"),
                "current_kernel_path": diagnosis_payload.get("current_kernel_path"),
                "recommended_direction_id": diagnosis_payload.get("recommended_direction_id"),
                "recommended_direction_name": next(
                    (
                        direction.get("name")
                        for direction in normalized_directions
                        if direction.get("direction_id")
                        == diagnosis_payload.get("recommended_direction_id")
                    ),
                    None,
                ),
                "family_audit": diagnosis_payload.get("family_audit") or [],
                "directions": normalized_directions,
                "notes": diagnosis_payload.get("notes"),
                "source_runtime_ms": run_payload.get("runtime_ms"),
                "source_tflops": run_payload.get("tflops"),
                "source_headline_metrics": run_payload.get("headline_metrics"),
                "selected_direction_id": payload_selected_direction_id or selected_direction_id,
                "selected_direction_name": payload_selected_direction_name or selected_direction_name,
                "selected_implementation_commit": selected_commit,
            }
        )
    return diagnosis_records


def attempt_payload_matches_direction(
    payload: dict[str, Any] | None,
    direction_id: str,
) -> bool:
    if not payload:
        return False
    payload_direction_id = payload.get("direction_id")
    if payload_direction_id:
        return payload_direction_id == direction_id
    return True


def resolve_attempt_state_payload(
    node_c_commit: str,
    measurement_commit: str | None,
    direction_id: str,
) -> dict[str, Any]:
    measurement_payload = load_json_at_commit(measurement_commit, "state/latest_attempt.json")
    if attempt_payload_matches_direction(measurement_payload, direction_id):
        return measurement_payload or {}
    node_c_payload = load_json_at_commit(node_c_commit, "state/latest_attempt.json")
    if attempt_payload_matches_direction(node_c_payload, direction_id):
        return node_c_payload or {}
    return {}


def resolve_active_direction_payload(node_c_commit: str) -> dict[str, Any]:
    return load_json_at_commit(node_c_commit, "state/active_direction.json") or {}


def build_attempt_records(
    node_c_commits: list[CommitRecord],
    diagnosis_records: list[dict[str, Any]],
    diagnosis_order_by_commit: dict[str, int],
    measurements_by_short: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for record in node_c_commits:
        match = NODE_C_SUBJECT_RE.match(record.subject)
        if not match:
            continue
        subject_meta = match.groupdict()
        sections = parse_sections(record.body)
        changed_kv, changed_plain = parse_key_value_bullets(sections.get("What changed", []))
        measurement_kv, _ = parse_key_value_bullets(sections.get("Measurement", []))
        touched_files = commit_touched_files(record.sha)
        parent_commit = commit_parent(record.sha)
        code_touched_files = [path for path in touched_files if not path.startswith("state/")]
        state_touched_files = [path for path in touched_files if path.startswith("state/")]
        linked_diagnosis = None
        linked_diagnosis_order = -1
        for diagnosis in diagnosis_records:
            diagnosis_order = diagnosis_order_by_commit.get(diagnosis["diagnosis_commit"], -1)
            if diagnosis_order < record.order and diagnosis_order > linked_diagnosis_order:
                linked_diagnosis = diagnosis
                linked_diagnosis_order = diagnosis_order
        measurement = measurements_by_short.get(record.short)
        attempt_status = "measured" if measurement else "build_only"
        measurement_commit = measurement.get("measurement_commit") if measurement else None
        linked_direction = next(
            (
                direction
                for direction in ((linked_diagnosis or {}).get("directions") or [])
                if direction.get("direction_id") == subject_meta["direction_id"]
            ),
            None,
        )
        attempt_state = resolve_attempt_state_payload(
            record.sha,
            measurement_commit,
            subject_meta["direction_id"],
        )
        active_direction_payload = resolve_active_direction_payload(record.sha)
        parent_state_run_id = (
            linked_diagnosis.get("source_run_id") if linked_diagnosis else None
        )
        family_id = first_non_null(
            attempt_state.get("family_id"),
            active_direction_payload.get("family_id"),
            linked_direction.get("family_id") if linked_direction else None,
        )
        subfamily_id = first_non_null(
            attempt_state.get("subfamily_id"),
            active_direction_payload.get("subfamily_id"),
            linked_direction.get("subfamily_id") if linked_direction else None,
        )
        planned_action_fingerprint = first_non_null(
            attempt_state.get("planned_action_fingerprint"),
            active_direction_payload.get("action_fingerprint"),
            linked_direction.get("action_fingerprint") if linked_direction else None,
        )
        if not planned_action_fingerprint and linked_direction:
            planned_action_fingerprint = make_action_fingerprint(linked_direction)
        implemented_action_fingerprint = first_non_null(
            attempt_state.get("implemented_action_fingerprint"),
            active_direction_payload.get("implemented_action_fingerprint"),
            planned_action_fingerprint,
        )
        semantic_delta_tags = (
            attempt_state.get("semantic_delta_tags")
            or derive_semantic_delta_tags_from_files(code_touched_files)
        )
        build_status = first_non_null(
            attempt_state.get("build_status"),
            (attempt_state.get("implementation") or {}).get("build_status"),
            measurement_kv.get("build"),
        )
        transition_label = first_non_null(
            attempt_state.get("transition_label"),
            derive_transition_label_from_measurement(
                parent_state_run_id,
                measurement,
                build_status,
                linked_direction.get("predicted_gain_ms") if linked_direction else None,
            ),
        )
        resource_snapshot = (
            (measurement or {}).get("resource_snapshot")
            or {
                "registers_per_thread": None,
                "shared_mem_per_block_allocated": None,
            }
        )
        family_ledger_payload = load_json_at_commit(
            measurement_commit or record.sha,
            "state/family_ledger.json",
        ) or {}
        family_ledger_snapshot = (
            ((family_ledger_payload.get("families") or {}).get(family_id))
            if family_id
            else None
        )
        family_status = (
            family_ledger_snapshot.get("freeze_status")
            if isinstance(family_ledger_snapshot, dict)
            else None
        )
        action_mode = first_non_null(
            attempt_state.get("mode"),
            linked_direction.get("mode") if linked_direction else None,
        )
        candidate_id = first_non_null(
            attempt_state.get("candidate_id"),
            active_direction_payload.get("candidate_id"),
        )
        base_run_id = first_non_null(
            attempt_state.get("base_run_id"),
            active_direction_payload.get("base_run_id"),
            parent_state_run_id,
        )
        default_result_state = {
            "measurement_commit": None,
            "measurement_commit_short": None,
            "measurement_subject": None,
            "measurement_order": None,
            "round_label": None,
            "run_id": None,
            "kernel_tag": f"bf16_gemm_v1_{record.short}",
            "previous_run_id": parent_state_run_id,
            "run_dir": None,
            "summary_json_path": None,
            "ncu_summary_json_path": None,
            "ncu_rep_path": None,
            "runtime_ms": None,
            "runtime_p10_ms": None,
            "runtime_p90_ms": None,
            "runtime_delta_ms": None,
            "runtime_delta_label": None,
            "tflops": None,
            "tflops_delta": None,
            "correctness": None,
            "tensor_pipe_active": None,
            "resource_snapshot": {
                "registers_per_thread": None,
                "shared_mem_per_block_allocated": None,
            },
            "headline_metrics": {},
            "headline_metric_deltas_vs_previous_run": {},
        }
        attempts.append(
            {
                "schema_version": SCHEMA_VERSION,
                "attempt_id": measurement["run_id"] if measurement else f"build_only_{record.short}",
                "round_label": subject_meta["round_label"],
                "status": attempt_status,
                "parent_state_run_id": parent_state_run_id,
                "diagnosis_commit": linked_diagnosis.get("diagnosis_commit")
                if linked_diagnosis
                else None,
                "diagnosis_recommended_direction_id": linked_diagnosis.get(
                    "recommended_direction_id"
                )
                if linked_diagnosis
                else None,
                "diagnosis_recommended_direction_name": linked_diagnosis.get(
                    "recommended_direction_name"
                )
                if linked_diagnosis
                else None,
                "candidate_id": candidate_id,
                "base_run_id": base_run_id,
                "family_id": family_id,
                "subfamily_id": subfamily_id,
                "mode": action_mode,
                "planned_action_fingerprint": planned_action_fingerprint,
                "implemented_action_fingerprint": implemented_action_fingerprint,
                "transition_label": transition_label,
                "semantic_delta_tags": semantic_delta_tags,
                "resource_snapshot": resource_snapshot,
                "family_status": family_status,
                "family_ledger_snapshot": family_ledger_snapshot,
                "action": {
                    "direction_id": subject_meta["direction_id"],
                    "direction_name": subject_meta["direction_name"],
                    "rank_in_diagnosis": linked_direction.get("rank")
                    if linked_direction
                    else None,
                    "was_recommended": (
                        subject_meta["direction_id"]
                        == linked_diagnosis.get("recommended_direction_id")
                    )
                    if linked_diagnosis
                    else None,
                    "selection_mode": changed_kv.get("selection mode"),
                    "idea_origin": changed_kv.get("idea origin"),
                    "motivation": changed_kv.get("implementation hypothesis"),
                    "expected_bottleneck": changed_kv.get("expected bottleneck"),
                    "code_locations": parse_list_field(changed_kv.get("code locations")),
                    "candidate_id": candidate_id,
                    "base_run_id": base_run_id,
                    "family_id": family_id,
                    "subfamily_id": subfamily_id,
                    "mode": action_mode,
                    "planned_action_fingerprint": planned_action_fingerprint,
                    "search_score_v1": linked_direction.get("search_score_v1")
                    if linked_direction
                    else None,
                    "score_breakdown": linked_direction.get("score_breakdown")
                    if linked_direction
                    else {},
                    "predicted_gain_ms": linked_direction.get("predicted_gain_ms")
                    if linked_direction
                    else None,
                    "predicted_fail_risk": linked_direction.get("predicted_fail_risk")
                    if linked_direction
                    else None,
                    "ranking_notes": linked_direction.get("ranking_notes")
                    if linked_direction
                    else [],
                },
                "implementation": {
                    "commit": record.sha,
                    "commit_short": record.short,
                    "subject": record.subject,
                    "parent_commit": parent_commit,
                    "diff_ref": f"{parent_commit}..{record.sha}" if parent_commit else record.sha,
                    "build_status": measurement_kv.get("build"),
                    "touched_files": touched_files,
                    "code_touched_files": code_touched_files,
                    "state_touched_files": state_touched_files,
                    "diff_stats": commit_diff_stats(record.sha),
                    "planned_action_fingerprint": planned_action_fingerprint,
                    "implemented_action_fingerprint": implemented_action_fingerprint,
                    "semantic_delta_tags": semantic_delta_tags,
                    "notes": changed_plain,
                },
                "result_state": measurement if measurement else default_result_state,
            }
        )
    return attempts


def build_order_lookup(records: list[CommitRecord]) -> dict[str, int]:
    return {record.sha: record.order for record in records}


def main() -> None:
    head_commit = git("rev-parse", "HEAD").strip()
    commit_stream = collect_commit_stream(head_commit)
    order_lookup = build_order_lookup(commit_stream)

    node_a_records = [record for record in commit_stream if record.node_type == "node_a"]
    node_b_records = [record for record in commit_stream if record.node_type == "node_b"]
    node_c_records = [record for record in commit_stream if record.node_type == "node_c"]

    measurements_by_short = build_node_a_map(node_a_records)
    diagnosis_records = build_diagnosis_records(node_b_records, node_c_records)

    def diagnosis_sort_key(record: dict[str, Any]) -> int:
        return order_lookup.get(record["diagnosis_commit"], -1)

    diagnosis_records.sort(key=diagnosis_sort_key)
    diagnosis_order_by_commit = {
        record["diagnosis_commit"]: order_lookup.get(record["diagnosis_commit"], -1)
        for record in diagnosis_records
    }
    attempts = build_attempt_records(
        node_c_records,
        diagnosis_records,
        diagnosis_order_by_commit,
        measurements_by_short,
    )
    attempts.sort(key=lambda record: order_lookup.get(record["implementation"]["commit"], -1))

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "head_commit": head_commit,
        "head_commit_short": head_commit[:7],
        "diagnosis_count": len(diagnosis_records),
        "attempt_count": len(attempts),
        "measured_attempt_count": sum(
            1 for attempt in attempts if attempt["status"] == "measured"
        ),
        "build_only_attempt_count": sum(
            1 for attempt in attempts if attempt["status"] == "build_only"
        ),
        "node_a_commit_count": len(node_a_records),
        "node_b_commit_count": len(node_b_records),
        "node_c_commit_count": len(node_c_records),
        "notes": (
            "This snapshot is pinned to one HEAD commit so concurrent local work "
            "does not change the exported history mid-run."
        ),
    }

    write_json(DATASET_DIR / "manifest.json", manifest)
    write_jsonl(DATASET_DIR / "diagnoses.jsonl", diagnosis_records)
    write_jsonl(DATASET_DIR / "attempts.jsonl", attempts)


if __name__ == "__main__":
    main()
