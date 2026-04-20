#!/usr/bin/env python3
"""Render an updated optimization tree from round_history.jsonl.

Outputs:
- matmul_optimization_tree_pretty.svg
- matmul_optimization_tree_pretty.png

The SVG is the primary artifact. PNG is rendered directly with Pillow so the
script stays offline-friendly and does not need cairosvg.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
import textwrap
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont


PALETTE = {
    "Async pipeline & staging": {
        "fill": "#E8F2FF",
        "stroke": "#2B6CB0",
        "text": "#123A67",
    },
    "Tiling & decomposition": {
        "fill": "#FFF2DE",
        "stroke": "#D97706",
        "text": "#7C3E00",
    },
    "Shared-memory layout": {
        "fill": "#F5EAFF",
        "stroke": "#9333EA",
        "text": "#5B1E8C",
    },
    "Hot-loop specialization": {
        "fill": "#E9F8F0",
        "stroke": "#0F9F6E",
        "text": "#0E5A42",
    },
    "Epilogue & data movement": {
        "fill": "#FFE9EE",
        "stroke": "#E11D48",
        "text": "#7A1130",
    },
    "Other": {
        "fill": "#F1F5F9",
        "stroke": "#64748B",
        "text": "#334155",
    },
}

EDGE_COLORS = {
    "improved": "#10B981",
    "regressed": "#F97316",
    "neutral": "#94A3B8",
    "goal": "#16A34A",
}

BACKGROUND = "#FBFCFE"
TITLE_COLOR = "#0F172A"
SUBTITLE_COLOR = "#334155"
MUTED = "#64748B"


def short_id(run_id: str) -> str:
    return run_id.split("_")[-1][:7]


def short_label(run_or_commit: str) -> str:
    value = run_or_commit.split("_")[-1]
    return value[:7]


def is_human(record: dict) -> bool:
    name = record.get("direction_name", "").lower()
    return (
        "human idea" in name
        or record.get("idea_origin") == "human-idea"
        or record.get("selection_mode") in {"human_idea", "approved"}
    )


def classify_family(name: str) -> str:
    lower = name.lower()
    if any(
        token in lower
        for token in [
            "epilogue",
            "writeback",
            "export",
            "thread-coarsen",
            "load/store",
            "pair stores",
            "vectorize transfers",
            "scratch",
        ]
    ):
        return "Epilogue & data movement"
    if any(
        token in lower
        for token in [
            "swizzle",
            "skew",
            "shared-memory",
            "shared tile",
            "shared",
            "bank-conflict",
            "feed path",
            "fragment delivery",
        ]
    ):
        return "Shared-memory layout"
    if any(
        token in lower
        for token in [
            "peeled",
            "steady-state",
            "prologue",
            "phase",
            "straight-line",
            "fixed-shape",
            "hot loop",
            "hot path",
            "register reuse",
            "row-pairs",
            "half-panel",
        ]
    ):
        return "Hot-loop specialization"
    if any(
        token in lower
        for token in [
            "retile",
            "cta",
            "warp",
            "main tiling",
            "main-kernel",
            "tile",
            "decomposition",
            "64x",
            "256x",
            "128x",
        ]
    ):
        return "Tiling & decomposition"
    if any(
        token in lower
        for token in [
            "async",
            "cp.async",
            "pipeline",
            "barrier",
            "stage",
            "staging",
            "producer",
            "consumer",
            "double-buffer",
            "prefetch",
            "overlap",
        ]
    ):
        return "Async pipeline & staging"
    return "Other"


def clean_direction_name(name: str) -> str:
    cleaned = re.sub(r"^Human idea\s+\d+\s*", "", name.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def load_records(path: Path) -> list[dict]:
    records = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    records.sort(key=lambda item: item["recorded_at"])
    return records


def parse_cutlass_ms(path: Path) -> float | None:
    if not path.exists():
        return None
    match = re.search(r"runtime:\s*`([0-9.]+)\s*ms`", path.read_text())
    if not match:
        return None
    return float(match.group(1))


def parse_benchmark_snapshot(path: Path) -> dict[str, str | float | None]:
    if not path.exists():
        return {}

    text = path.read_text()
    snapshot: dict[str, str | float | None] = {}

    cutlass_match = re.search(r"## CUTLASS baseline.*?- runtime:\s*`([0-9.]+)\s*ms`", text, re.S)
    if cutlass_match:
        snapshot["cutlass_ms"] = float(cutlass_match.group(1))

    best_custom_match = re.search(r"## Best custom kernel.*?- runtime:\s*`([0-9.]+)\s*ms`", text, re.S)
    if best_custom_match:
        snapshot["best_custom_ms"] = float(best_custom_match.group(1))

    best_commit_match = re.search(r"## Best custom kernel.*?- measured commit:\s*`([0-9a-f]+)`", text, re.S)
    if best_commit_match:
        snapshot["best_custom_commit"] = best_commit_match.group(1)

    return snapshot


def discover_mainline(records: list[dict]) -> list[dict]:
    mainline: list[dict] = []
    best = float("inf")
    for record in records:
        if not record.get("correctness_passed", True):
            continue
        runtime = record["median_runtime_ms"]
        if runtime < best:
            best = runtime
            mainline.append(record)
    if mainline:
        return mainline
    return records[:1]


def pick_best_record(
    records: list[dict],
    official_best_ms: float | None,
    official_best_commit: str | None,
) -> dict:
    valid_records = [record for record in records if record.get("correctness_passed", True)]
    if not valid_records:
        valid_records = records

    if official_best_commit:
        for record in valid_records:
            if record.get("measured_commit") == official_best_commit:
                return record

    if official_best_ms is not None:
        candidate = min(valid_records, key=lambda item: abs(item["median_runtime_ms"] - official_best_ms))
        if abs(candidate["median_runtime_ms"] - official_best_ms) < 1e-3:
            return candidate

    return min(valid_records, key=lambda item: item["median_runtime_ms"])


def infer_external_bases(records: list[dict], record_by_id: dict[str, dict]) -> dict[str, dict]:
    external_children: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        prev = record.get("previous_run_id")
        if prev and prev not in record_by_id:
            external_children[prev].append(record)

    external_bases: dict[str, dict] = {}
    for prev, children in external_children.items():
        children.sort(key=lambda item: item["recorded_at"])
        first_child = children[0]
        runtime = first_child["median_runtime_ms"] - first_child.get("runtime_delta_ms", 0.0)
        external_bases[prev] = {
            "prev_id": prev,
            "runtime_ms": runtime,
            "first_child_run_id": first_child["run_id"],
            "first_child_index": first_child["_order_index"],
            "node_id": f"synthetic:{prev}",
        }
    return external_bases


def trace_anchor(
    previous_run_id: str | None,
    record_by_id: dict[str, dict],
    mainline_ids: set[str],
    external_bases: dict[str, dict],
) -> str | None:
    current = previous_run_id
    seen: set[str] = set()
    while current and current not in seen:
        seen.add(current)
        if current in mainline_ids:
            return current
        if current in external_bases:
            return external_bases[current]["node_id"]
        parent = record_by_id.get(current)
        if not parent:
            return None
        current = parent.get("previous_run_id")
    return None


def pick_side_map(mainline: list[dict]) -> dict[str, str]:
    side_map: dict[str, str] = {}
    sides = ["left", "right"]
    for index, record in enumerate(mainline):
        side_map[record["run_id"]] = sides[index % 2]
    return side_map


def resolve_lane_overlaps(nodes: dict[str, dict], node_ids: list[str], min_gap: float) -> None:
    """Shift nodes downward within a visual lane until boxes no longer overlap."""
    last_bottom: float | None = None
    for node_id in sorted(node_ids, key=lambda current_id: nodes[current_id]["y"]):
        node = nodes[node_id]
        if last_bottom is not None:
            node["y"] = max(node["y"], last_bottom + min_gap)
        last_bottom = node["y"] + node["h"]


def build_graph(
    records: list[dict],
    baseline_ms: float,
    cutlass_ms: float,
    official_best_ms: float | None = None,
    official_best_commit: str | None = None,
) -> tuple[dict, list[tuple[str, str, str, str]]]:
    for index, record in enumerate(records):
        record["_order_index"] = index

    record_by_id = {record["run_id"]: record for record in records}
    mainline = discover_mainline(records)
    mainline_ids = {record["run_id"] for record in mainline}
    external_bases = infer_external_bases(records, record_by_id)
    side_map = pick_side_map(mainline)

    anchor_of_record: dict[str, str | None] = {}
    for record in records:
        if record["run_id"] not in mainline_ids:
            anchor_of_record[record["run_id"]] = trace_anchor(
                record.get("previous_run_id"), record_by_id, mainline_ids, external_bases
            )

    synthetic_parent: dict[str, str] = {}
    for prev, base in external_bases.items():
        first_child = record_by_id[base["first_child_run_id"]]
        if first_child in mainline:
            synthetic_parent[base["node_id"]] = "baseline"
            continue
        parent_anchor = None
        first_child_index = first_child["_order_index"]
        for candidate in mainline:
            if candidate["_order_index"] < first_child_index:
                parent_anchor = candidate["run_id"]
        synthetic_parent[base["node_id"]] = parent_anchor or "baseline"

    width = 1800
    center_x = 900
    trunk_w = 420
    side_w = 370
    baseline_h = 84
    root_h = 74
    trunk_h = 86
    side_h = 78
    top = 270
    step = 68
    side_left_x = 110
    side_right_x = width - side_w - 110
    provisional_height = top + max(8, len(records) + 4) * step + 190

    def slot_y(order_index: int) -> float:
        return top + order_index * step

    nodes: dict[str, dict] = {}

    best_record = pick_best_record(records, official_best_ms=official_best_ms, official_best_commit=official_best_commit)
    best_runtime_ms = official_best_ms if official_best_ms is not None else best_record["median_runtime_ms"]
    subtitle = (
        f"Current best custom kernel: {best_runtime_ms:.2f} ms"
        f" | CUTLASS: {cutlass_ms:.2f} ms"
        f" | start: {baseline_ms:.2f} ms"
    )

    nodes["baseline"] = {
        "x": center_x - trunk_w / 2,
        "y": 118,
        "w": trunk_w,
        "h": baseline_h,
        "fill": "#FFF1E6",
        "stroke": "#F97316",
        "text": "#8A2C0D",
        "family": "Starting point",
        "headline": f"start | {baseline_ms:.2f} ms",
        "lines": ["User-reported early naive kernel before the tracked round history."],
        "human": False,
        "synthetic": False,
        "special": True,
    }

    first_main = mainline[0]
    first_prev = first_main.get("previous_run_id")
    root_external = external_bases.get(first_prev)
    if root_external:
        nodes[root_external["node_id"]] = {
            "x": center_x - trunk_w / 2,
            "y": 188,
            "w": trunk_w,
            "h": root_h,
            "fill": "#F8FAFC",
            "stroke": "#94A3B8",
            "text": "#475569",
            "family": "Accepted base",
            "headline": f"base {short_label(first_prev)} | {root_external['runtime_ms']:.2f} ms",
            "lines": ["Accepted tensor-core base outside the tracked round-history window."],
            "human": False,
            "synthetic": True,
            "special": False,
        }

    group_side: dict[str, str] = {}
    for node_id, parent in synthetic_parent.items():
        if parent in side_map:
            group_side[node_id] = side_map[parent]
        else:
            group_side[node_id] = "right"

    for record in records:
        family = classify_family(record["direction_name"])
        palette = PALETTE[family]
        is_main = record["run_id"] in mainline_ids
        side = None
        if not is_main:
            anchor = anchor_of_record[record["run_id"]]
            if anchor in group_side:
                side = group_side[anchor]
            elif anchor in side_map:
                side = side_map[anchor]
            else:
                side = "left"

        node_w = trunk_w if is_main else side_w
        node_h = trunk_h if is_main else side_h
        node_x = center_x - node_w / 2
        if not is_main and side == "left":
            node_x = side_left_x
        if not is_main and side == "right":
            node_x = side_right_x

        lines = textwrap.wrap(clean_direction_name(record["direction_name"]), width=44 if is_main else 34)[:2]
        nodes[record["run_id"]] = {
            "x": node_x,
            "y": slot_y(record["_order_index"]),
            "w": node_w,
            "h": node_h,
            "fill": palette["fill"],
            "stroke": palette["stroke"],
            "text": palette["text"],
            "family": family,
            "headline": (
                f"R{record['round_index']:02d} | {short_id(record['run_id'])}"
                f" | {record['median_runtime_ms']:.2f} ms"
            ),
            "lines": lines,
            "human": is_human(record),
            "synthetic": False,
            "special": record["run_id"] == best_record["run_id"],
        }

    synthetic_layout_order = sorted(
        (base for base in external_bases.values() if base["node_id"] in group_side),
        key=lambda item: item["first_child_index"],
    )
    used_side_bottom = {"left": 210.0, "right": 210.0}
    for base in synthetic_layout_order:
        node_id = base["node_id"]
        if node_id in nodes:
            continue
        side = group_side[node_id]
        desired_y = slot_y(base["first_child_index"]) - root_h - 26
        y = max(desired_y, used_side_bottom[side] + 18)
        used_side_bottom[side] = y + root_h
        x = side_left_x if side == "left" else side_right_x
        nodes[node_id] = {
            "x": x,
            "y": y,
            "w": side_w,
            "h": root_h,
            "fill": "#F8FAFC",
            "stroke": "#94A3B8",
            "text": "#475569",
            "family": "Accepted base",
            "headline": f"base {short_label(base['prev_id'])} | {base['runtime_ms']:.2f} ms",
            "lines": ["Restored accepted base outside the tracked round-history window."],
            "human": False,
            "synthetic": True,
            "special": False,
        }

    center_lane_ids = [
        node_id
        for node_id, node in nodes.items()
        if abs(node["x"] - (center_x - trunk_w / 2)) < 1e-6
    ]
    left_lane_ids = [node_id for node_id, node in nodes.items() if abs(node["x"] - side_left_x) < 1e-6]
    right_lane_ids = [node_id for node_id, node in nodes.items() if abs(node["x"] - side_right_x) < 1e-6]

    resolve_lane_overlaps(nodes, center_lane_ids, min_gap=18)
    resolve_lane_overlaps(nodes, left_lane_ids, min_gap=16)
    resolve_lane_overlaps(nodes, right_lane_ids, min_gap=16)

    content_bottom = max(node["y"] + node["h"] for node in nodes.values())
    cutlass_y = max(content_bottom + 140, provisional_height - 118)
    height = cutlass_y + 78 + 70

    nodes["cutlass"] = {
        "x": center_x - 190,
        "y": cutlass_y,
        "w": 380,
        "h": 78,
        "fill": "#ECFDF5",
        "stroke": "#16A34A",
        "text": "#14532D",
        "family": "Reference target",
        "headline": f"CUTLASS | {cutlass_ms:.2f} ms",
        "lines": ["Local baseline to beat on the same fixed BF16 GEMM benchmark."],
        "human": False,
        "synthetic": False,
        "special": True,
    }

    edges: list[tuple[str, str, str, str]] = []
    if root_external:
        edges.append(("baseline", root_external["node_id"], "neutral", "pre-history"))
        edges.append((root_external["node_id"], first_main["run_id"], "improved", ""))
    else:
        edges.append(("baseline", first_main["run_id"], "improved", "pre-history"))

    for prev_record, next_record in zip(mainline, mainline[1:]):
        edges.append((prev_record["run_id"], next_record["run_id"], "improved", ""))

    for node_id, parent in synthetic_parent.items():
        if node_id == root_external["node_id"] if root_external else False:
            continue
        edges.append((parent, node_id, "neutral", "restore"))

    for record in records:
        if record["run_id"] in mainline_ids:
            continue
        prev = record.get("previous_run_id")
        if prev in record_by_id:
            parent = prev
        elif prev in external_bases:
            parent = external_bases[prev]["node_id"]
        else:
            parent = anchor_of_record[record["run_id"]] or "baseline"
        kind = record.get("perf_verdict") or "neutral"
        if kind not in EDGE_COLORS:
            kind = "neutral"
        edges.append((parent, record["run_id"], kind, ""))

    gap = best_runtime_ms - cutlass_ms
    edges.append((best_record["run_id"], "cutlass", "goal", f"gap {gap:.2f} ms"))

    meta = {
        "width": width,
        "height": height,
        "subtitle": subtitle,
        "best_runtime_ms": best_runtime_ms,
    }
    return {"nodes": nodes, "edges": edges, "meta": meta}, mainline


def edge_path(a: dict, b: dict) -> str:
    if a["x"] + a["w"] < b["x"]:
        x1 = a["x"] + a["w"]
        y1 = a["y"] + a["h"] / 2
        x2 = b["x"]
        y2 = b["y"] + b["h"] / 2
    elif b["x"] + b["w"] < a["x"]:
        x1 = a["x"]
        y1 = a["y"] + a["h"] / 2
        x2 = b["x"] + b["w"]
        y2 = b["y"] + b["h"] / 2
    else:
        x1 = a["x"] + a["w"] / 2
        y1 = a["y"] + a["h"]
        x2 = b["x"] + b["w"] / 2
        y2 = b["y"]

    dx = (x2 - x1) * 0.42
    if abs(x2 - x1) < 60:
        c1x, c1y = x1, y1 + 36
        c2x, c2y = x2, y2 - 36
    else:
        c1x, c1y = x1 + dx, y1
        c2x, c2y = x2 - dx, y2
    return f"M {x1:.1f},{y1:.1f} C {c1x:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} {x2:.1f},{y2:.1f}"


def cubic_points(a: dict, b: dict, segments: int = 28) -> list[tuple[float, float]]:
    if a["x"] + a["w"] < b["x"]:
        p0 = (a["x"] + a["w"], a["y"] + a["h"] / 2)
        p3 = (b["x"], b["y"] + b["h"] / 2)
    elif b["x"] + b["w"] < a["x"]:
        p0 = (a["x"], a["y"] + a["h"] / 2)
        p3 = (b["x"] + b["w"], b["y"] + b["h"] / 2)
    else:
        p0 = (a["x"] + a["w"] / 2, a["y"] + a["h"])
        p3 = (b["x"] + b["w"] / 2, b["y"])

    dx = (p3[0] - p0[0]) * 0.42
    if abs(p3[0] - p0[0]) < 60:
        p1 = (p0[0], p0[1] + 36)
        p2 = (p3[0], p3[1] - 36)
    else:
        p1 = (p0[0] + dx, p0[1])
        p2 = (p3[0] - dx, p3[1])

    points = []
    for step in range(segments + 1):
        t = step / segments
        omt = 1.0 - t
        x = (
            omt ** 3 * p0[0]
            + 3 * omt * omt * t * p1[0]
            + 3 * omt * t * t * p2[0]
            + t ** 3 * p3[0]
        )
        y = (
            omt ** 3 * p0[1]
            + 3 * omt * omt * t * p1[1]
            + 3 * omt * t * t * p2[1]
            + t ** 3 * p3[1]
        )
        points.append((x, y))
    return points


def star_points(cx: float, cy: float, radius: float) -> list[tuple[float, float]]:
    points = []
    for index in range(10):
        angle = -math.pi / 2 + index * math.pi / 5
        current_radius = radius if index % 2 == 0 else radius * 0.45
        points.append((cx + math.cos(angle) * current_radius, cy + math.sin(angle) * current_radius))
    return points


def wrap_svg_text(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width)


def svg_text(x: float, y: float, content: str, size: int, weight: int, fill: str, anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="DejaVu Sans, Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">'
        f"{html.escape(content)}</text>"
    )


def draw_svg_badge(x: float, y: float) -> str:
    star = " ".join(f"{px:.1f},{py:.1f}" for px, py in star_points(x + 14, y + 11, 7))
    parts = [
        f'<rect x="{x}" y="{y}" width="96" height="24" rx="12" fill="#FFF7ED" stroke="#D97706" stroke-width="1.2"/>',
        f'<polygon points="{star}" fill="#D97706"/>',
        svg_text(x + 58, y + 16, "human idea", 10, 700, "#B45309", anchor="middle"),
    ]
    return "\n".join(parts)


def render_svg(graph: dict, mainline: list[dict]) -> str:
    nodes = graph["nodes"]
    edges = graph["edges"]
    width = graph["meta"]["width"]
    height = graph["meta"]["height"]
    subtitle = graph["meta"]["subtitle"]

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        """
<defs>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0f172a" flood-opacity="0.08"/>
  </filter>
  <marker id="arrow-improved" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#10B981"/>
  </marker>
  <marker id="arrow-regressed" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#F97316"/>
  </marker>
  <marker id="arrow-neutral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#94A3B8"/>
  </marker>
  <marker id="arrow-goal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#16A34A"/>
  </marker>
</defs>
""",
        f'<rect width="{width}" height="{height}" fill="{BACKGROUND}"/>',
        svg_text(64, 52, "matmul_optimizer optimization tree", 28, 800, TITLE_COLOR),
        svg_text(64, 82, subtitle, 14, 600, SUBTITLE_COLOR),
        svg_text(
            64,
            104,
            "Main vertical spine = new best correct-so-far milestones. Side branches = other attempts grouped under the nearest accepted base.",
            13,
            500,
            SUBTITLE_COLOR,
        ),
        svg_text(
            64,
            124,
            "Fixed BF16 GEMM on RTX 3070 Laptop GPU. Colors show optimization families. Dashed gray edges mark restores or pre-history handoffs.",
            13,
            500,
            SUBTITLE_COLOR,
        ),
    ]

    legend_x = 980
    legend_y = 42
    legend_items = [name for name in PALETTE if name != "Other"]
    for index, family in enumerate(legend_items):
        palette = PALETTE[family]
        x = legend_x + (index % 2) * 270
        y = legend_y + (index // 2) * 36
        svg_parts.append(
            f'<rect x="{x}" y="{y}" width="244" height="24" rx="12" fill="{palette["fill"]}" stroke="{palette["stroke"]}" stroke-width="1.3"/>'
        )
        svg_parts.append(svg_text(x + 122, y + 16, family, 11, 700, palette["text"], anchor="middle"))
    svg_parts.append(draw_svg_badge(legend_x, legend_y + 74))
    svg_parts.append(
        f'<rect x="{legend_x + 126}" y="{legend_y + 74}" width="210" height="24" rx="12" fill="#ECFDF5" stroke="#10B981" stroke-width="1.3"/>'
    )
    svg_parts.append(svg_text(legend_x + 231, legend_y + 90, "green edge = improved", 11, 700, "#047857", anchor="middle"))
    svg_parts.append(
        f'<rect x="{legend_x + 350}" y="{legend_y + 74}" width="226" height="24" rx="12" fill="#FFF7ED" stroke="#F97316" stroke-width="1.3"/>'
    )
    svg_parts.append(svg_text(legend_x + 463, legend_y + 90, "orange edge = regressed", 11, 700, "#C2410C", anchor="middle"))

    for src, dst, kind, label in edges:
        color = EDGE_COLORS[kind]
        dash = ' stroke-dasharray="7 6"' if kind in {"neutral", "goal"} else ""
        marker = f"arrow-{kind}"
        svg_parts.append(
            f'<path d="{edge_path(nodes[src], nodes[dst])}" fill="none" stroke="{color}" stroke-width="2.4"{dash} marker-end="url(#{marker})"/>'
        )
        if label:
            a = nodes[src]
            b = nodes[dst]
            mx = (a["x"] + a["w"] / 2 + b["x"] + b["w"] / 2) / 2
            my = (a["y"] + a["h"] / 2 + b["y"] + b["h"] / 2) / 2 - 8
            svg_parts.append(f'<rect x="{mx - 42}" y="{my - 12}" width="84" height="20" rx="10" fill="#FFFFFF" fill-opacity="0.92"/>')
            svg_parts.append(svg_text(mx, my + 2, label, 10, 700, color, anchor="middle"))

    ordered_nodes = sorted(nodes.items(), key=lambda item: (item[1]["y"], item[1]["x"]))
    for node_id, node in ordered_nodes:
        dash = ' stroke-dasharray="7 6"' if node.get("synthetic") else ""
        filter_attr = ' filter="url(#shadow)"' if not node.get("synthetic") else ""
        svg_parts.append(
            f'<rect x="{node["x"]}" y="{node["y"]}" width="{node["w"]}" height="{node["h"]}" rx="18" '
            f'fill="{node["fill"]}" stroke="{node["stroke"]}" stroke-width="2.1"{dash}{filter_attr}/>'
        )
        if node.get("special") and node_id not in {"baseline", "cutlass"}:
            svg_parts.append(
                f'<rect x="{node["x"] - 4}" y="{node["y"] - 4}" width="{node["w"] + 8}" height="{node["h"] + 8}" '
                f'rx="22" fill="none" stroke="{node["stroke"]}" stroke-width="1.3" stroke-opacity="0.55"/>'
            )
        svg_parts.append(svg_text(node["x"] + 18, node["y"] + 20, node["family"], 10, 700, node["text"]))
        svg_parts.append(svg_text(node["x"] + 18, node["y"] + 42, node["headline"], 16, 800, node["text"]))
        text_y = node["y"] + 62
        for line in wrap_svg_text(" ".join(node["lines"]), width=46 if node["w"] > 400 else 36)[:2]:
            svg_parts.append(svg_text(node["x"] + 18, text_y, line, 11, 500, node["text"]))
            text_y += 15
        if node.get("human"):
            svg_parts.append(draw_svg_badge(node["x"] + node["w"] - 110, node["y"] + 10))

    svg_parts.append(
        svg_text(
            width - 64,
            height - 22,
            "Auto-generated from state/round_history.jsonl + state/benchmark_baselines.md",
            11,
            500,
            MUTED,
            anchor="end",
        )
    )
    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def find_font(bold: bool = False) -> str | None:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/TTF/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return None


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    font_path = find_font(bold=bold)
    if font_path:
        return ImageFont.truetype(font_path, size=size)
    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    text: str,
    font: ImageFont.ImageFont,
    fill: str,
) -> None:
    width, height = text_size(draw, text, font)
    x0, y0, x1, y1 = box
    x = x0 + (x1 - x0 - width) / 2
    y = y0 + (y1 - y0 - height) / 2 - 1
    draw.text((x, y), text, font=font, fill=fill)


def draw_badge_png(draw: ImageDraw.ImageDraw, x: float, y: float, fonts: dict[str, ImageFont.ImageFont]) -> None:
    draw.rounded_rectangle((x, y, x + 96, y + 24), radius=12, fill="#FFF7ED", outline="#D97706", width=1)
    draw.polygon(star_points(x + 14, y + 12, 7), fill="#D97706")
    draw_centered_text(draw, (x + 24, y, x + 96, y + 24), "human idea", fonts["badge"], "#B45309")


def draw_arrow_head(draw: ImageDraw.ImageDraw, end: tuple[float, float], prev: tuple[float, float], color: str) -> None:
    angle = math.atan2(end[1] - prev[1], end[0] - prev[0])
    size = 8
    left = (
        end[0] - math.cos(angle) * size - math.sin(angle) * size * 0.55,
        end[1] - math.sin(angle) * size + math.cos(angle) * size * 0.55,
    )
    right = (
        end[0] - math.cos(angle) * size + math.sin(angle) * size * 0.55,
        end[1] - math.sin(angle) * size - math.cos(angle) * size * 0.55,
    )
    draw.polygon([end, left, right], fill=color)


def render_png(graph: dict, output_path: Path) -> None:
    nodes = graph["nodes"]
    edges = graph["edges"]
    width = graph["meta"]["width"]
    height = graph["meta"]["height"]
    subtitle = graph["meta"]["subtitle"]

    image = Image.new("RGBA", (width, height), ImageColor.getrgb(BACKGROUND))
    draw = ImageDraw.Draw(image)

    fonts = {
        "title": load_font(28, bold=True),
        "subtitle": load_font(14, bold=False),
        "family": load_font(10, bold=True),
        "headline": load_font(16, bold=True),
        "body": load_font(11, bold=False),
        "badge": load_font(10, bold=True),
        "footnote": load_font(11, bold=False),
        "legend": load_font(11, bold=True),
    }

    draw.text((64, 44), "matmul_optimizer optimization tree", font=fonts["title"], fill=TITLE_COLOR)
    draw.text((64, 76), subtitle, font=fonts["subtitle"], fill=SUBTITLE_COLOR)
    draw.text(
        (64, 98),
        "Main vertical spine = new best correct-so-far milestones. Side branches = other attempts grouped under the nearest accepted base.",
        font=fonts["subtitle"],
        fill=SUBTITLE_COLOR,
    )
    draw.text(
        (64, 118),
        "Fixed BF16 GEMM on RTX 3070 Laptop GPU. Colors show optimization families. Dashed gray edges mark restores or pre-history handoffs.",
        font=fonts["subtitle"],
        fill=SUBTITLE_COLOR,
    )

    legend_x = 980
    legend_y = 42
    legend_items = [name for name in PALETTE if name != "Other"]
    for index, family in enumerate(legend_items):
        palette = PALETTE[family]
        x = legend_x + (index % 2) * 270
        y = legend_y + (index // 2) * 36
        draw.rounded_rectangle((x, y, x + 244, y + 24), radius=12, fill=palette["fill"], outline=palette["stroke"], width=1)
        draw_centered_text(draw, (x, y, x + 244, y + 24), family, fonts["legend"], palette["text"])
    draw_badge_png(draw, legend_x, legend_y + 74, fonts)
    draw.rounded_rectangle((legend_x + 126, legend_y + 74, legend_x + 336, legend_y + 98), radius=12, fill="#ECFDF5", outline="#10B981", width=1)
    draw_centered_text(draw, (legend_x + 126, legend_y + 74, legend_x + 336, legend_y + 98), "green edge = improved", fonts["legend"], "#047857")
    draw.rounded_rectangle((legend_x + 350, legend_y + 74, legend_x + 576, legend_y + 98), radius=12, fill="#FFF7ED", outline="#F97316", width=1)
    draw_centered_text(draw, (legend_x + 350, legend_y + 74, legend_x + 576, legend_y + 98), "orange edge = regressed", fonts["legend"], "#C2410C")

    for src, dst, kind, label in edges:
        color = EDGE_COLORS[kind]
        points = cubic_points(nodes[src], nodes[dst])
        if kind in {"neutral", "goal"}:
            segment = 0
            while segment < len(points) - 1:
                if segment % 2 == 0:
                    draw.line([points[segment], points[min(segment + 1, len(points) - 1)]], fill=color, width=3)
                segment += 1
        else:
            draw.line(points, fill=color, width=3)
        draw_arrow_head(draw, points[-1], points[-2], color)
        if label:
            a = nodes[src]
            b = nodes[dst]
            mx = (a["x"] + a["w"] / 2 + b["x"] + b["w"] / 2) / 2
            my = (a["y"] + a["h"] / 2 + b["y"] + b["h"] / 2) / 2 - 8
            draw.rounded_rectangle((mx - 42, my - 12, mx + 42, my + 8), radius=10, fill="#FFFFFF", outline=None)
            draw_centered_text(draw, (mx - 42, my - 12, mx + 42, my + 8), label, fonts["badge"], color)

    ordered_nodes = sorted(nodes.items(), key=lambda item: (item[1]["y"], item[1]["x"]))
    for node_id, node in ordered_nodes:
        x0, y0 = node["x"], node["y"]
        x1, y1 = x0 + node["w"], y0 + node["h"]
        if not node.get("synthetic"):
            draw.rounded_rectangle((x0 + 3, y0 + 6, x1 + 3, y1 + 6), radius=18, fill=(15, 23, 42, 18))
        draw.rounded_rectangle((x0, y0, x1, y1), radius=18, fill=node["fill"], outline=node["stroke"], width=2)
        if node.get("special") and node_id not in {"baseline", "cutlass"}:
            draw.rounded_rectangle((x0 - 4, y0 - 4, x1 + 4, y1 + 4), radius=22, outline=node["stroke"], width=1)
        draw.text((x0 + 18, y0 + 9), node["family"], font=fonts["family"], fill=node["text"])
        draw.text((x0 + 18, y0 + 28), node["headline"], font=fonts["headline"], fill=node["text"])
        text_y = y0 + 50
        for line in textwrap.wrap(" ".join(node["lines"]), width=46 if node["w"] > 400 else 36)[:2]:
            draw.text((x0 + 18, text_y), line, font=fonts["body"], fill=node["text"])
            text_y += 14
        if node.get("human"):
            draw_badge_png(draw, x1 - 110, y0 + 10, fonts)

    footer = "Auto-generated from state/round_history.jsonl + state/benchmark_baselines.md"
    footer_w, _ = text_size(draw, footer, fonts["footnote"])
    draw.text((width - 64 - footer_w, height - 28), footer, font=fonts["footnote"], fill=MUTED)
    image.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to state/round_history.jsonl")
    parser.add_argument("--output-dir", default=".", help="Directory for SVG and PNG outputs")
    parser.add_argument("--baseline-ms", type=float, default=802.8426, help="Starting runtime before tracked rounds")
    parser.add_argument(
        "--cutlass-ms",
        type=float,
        default=None,
        help="CUTLASS runtime in ms. If omitted, try parsing benchmark_baselines.md",
    )
    parser.add_argument(
        "--cutlass-state",
        default=None,
        help="Optional path to benchmark_baselines.md for CUTLASS auto-detection",
    )
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    benchmark_snapshot: dict[str, str | float | None] = {}
    if args.cutlass_state:
        benchmark_snapshot = parse_benchmark_snapshot(Path(args.cutlass_state).resolve())

    cutlass_ms = args.cutlass_ms
    if cutlass_ms is None and benchmark_snapshot.get("cutlass_ms") is not None:
        cutlass_ms = float(benchmark_snapshot["cutlass_ms"])
    if cutlass_ms is None and args.cutlass_state:
        cutlass_ms = parse_cutlass_ms(Path(args.cutlass_state).resolve())
    if cutlass_ms is None:
        cutlass_ms = 25.917889

    records = load_records(input_path)
    graph, mainline = build_graph(
        records,
        baseline_ms=args.baseline_ms,
        cutlass_ms=cutlass_ms,
        official_best_ms=(
            float(benchmark_snapshot["best_custom_ms"])
            if benchmark_snapshot.get("best_custom_ms") is not None
            else None
        ),
        official_best_commit=(
            str(benchmark_snapshot["best_custom_commit"])
            if benchmark_snapshot.get("best_custom_commit") is not None
            else None
        ),
    )

    svg_path = output_dir / "matmul_optimization_tree_pretty.svg"
    png_path = output_dir / "matmul_optimization_tree_pretty.png"

    svg_path.write_text(render_svg(graph, mainline))
    render_png(graph, png_path)

    print(f"wrote {svg_path}")
    print(f"wrote {png_path}")


if __name__ == "__main__":
    main()
