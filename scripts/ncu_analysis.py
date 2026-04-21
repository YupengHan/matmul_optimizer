#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import textwrap
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


SCHEMA_VERSION = 2
TOP_FINDING_LIMIT = 6
TOP_HOTSPOT_LIMIT = 8

STALL_LABELS = {
    'smsp__warp_issue_stalled_barrier_per_warp_active.pct': 'barrier',
    'smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct': 'long_scoreboard',
    'smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct': 'short_scoreboard',
    'smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct': 'mio_throttle',
}

HIGHER_IS_BETTER_TOKENS = (
    'throughput',
    'active',
    'occupancy',
    'warps_active',
    'ipc',
    'utilization',
    'hit_rate',
)

LOWER_IS_BETTER_TOKENS = (
    'stall',
    'bank',
    'conflict',
    'scoreboard',
    'barrier',
    'throttle',
    'sectors_miss',
    'replay',
)

PERCENT_LIKE_UNITS = {'%'}
RAW_TOTAL_UNITS = {
    'cycle',
    'thread',
    'warp',
    'block',
    'byte',
    'kbyte',
    'kbyte/block',
    'byte/block',
}

LOW_SIGNAL_SECTION_METRICS = {
    'block size',
    'grid size',
    'threads',
    '# sms',
    'waves per sm',
    'elapsed cycles',
    'total dram elapsed cycles',
    'total l1 elapsed cycles',
    'total l2 elapsed cycles',
    'total sm elapsed cycles',
    'total smsp elapsed cycles',
    'average dram active cycles',
    'average l1 active cycles',
    'average l2 active cycles',
    'average sm active cycles',
    'average smsp active cycles',
}


def _relativize_path(path: Optional[Path], base: Optional[Path]) -> Optional[str]:
    if path is None:
        return None
    path = Path(path)
    if base is not None:
        try:
            return path.relative_to(base).as_posix()
        except ValueError:
            pass
    if path.is_absolute():
        return path.as_posix()
    return path.as_posix()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + '\n', encoding='utf-8')


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding='utf-8')


def parse_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        if isinstance(value, float) and not math.isfinite(value):
            return None
        return float(value)
    text = str(value).strip()
    if not text or text.lower() in {'n/a', 'none', 'nan'}:
        return None
    cleaned = text.replace(',', '')
    if cleaned.endswith('%'):
        cleaned = cleaned[:-1]
    try:
        parsed = float(cleaned)
    except ValueError:
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def numeric_or_text(value: Any) -> Any:
    parsed = parse_float(value)
    if parsed is not None:
        return parsed
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def slugify(text: Any) -> str:
    seed = str(text or '').strip().lower()
    pieces: List[str] = []
    last_sep = False
    for char in seed:
        if char.isalnum():
            pieces.append(char)
            last_sep = False
        elif not last_sep:
            pieces.append('_')
            last_sep = True
    slug = ''.join(pieces).strip('_')
    return slug or 'unknown'


def read_filtered_csv_lines(path: Optional[Path]) -> List[str]:
    if path is None or not Path(path).exists():
        return []
    filtered: List[str] = []
    for raw in Path(path).read_text(encoding='utf-8', errors='replace').splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith('==PROF=='):
            continue
        filtered.append(raw)
    return filtered


def source_page_is_disassembly(path: Optional[Path]) -> bool:
    rows = read_csv_matrix(path)
    if len(rows) < 2:
        return False
    header = [str(cell).strip() for cell in rows[1]]
    return header == ['Address', 'Source']


def read_csv_matrix(path: Optional[Path]) -> List[List[str]]:
    lines = read_filtered_csv_lines(path)
    if not lines:
        return []
    return [[cell.strip() for cell in row] for row in csv.reader(io.StringIO('\n'.join(lines)))]


def is_units_row(row: Sequence[str]) -> bool:
    if not row:
        return False
    unit_like_tokens = {
        '',
        '%',
        'cycle',
        'cycle/nsecond',
        'block',
        'byte',
        'byte/block',
        'register/thread',
        'Kbyte',
        'Kbyte/block',
        'warp',
        'thread',
        'SM',
        'pass',
        'nsecond',
    }
    hits = 0
    for cell in row:
        token = str(cell).strip()
        if token in unit_like_tokens:
            hits += 1
            continue
        if token.isalpha() and len(token) <= 12:
            hits += 1
    return hits >= max(3, int(len(row) * 0.6))


def parse_wide_csv_records(path: Optional[Path]) -> List[Dict[str, str]]:
    rows = read_csv_matrix(path)
    if not rows:
        return []

    header_idx = None
    for idx, row in enumerate(rows):
        if 'ID' in row and 'Kernel Name' in row:
            header_idx = idx
            break
    if header_idx is None:
        return []

    header = rows[header_idx]
    candidate_rows = rows[header_idx + 1:]
    if candidate_rows and is_units_row(candidate_rows[0]):
        candidate_rows = candidate_rows[1:]

    records: List[Dict[str, str]] = []
    for row in candidate_rows:
        if len(row) != len(header):
            continue
        if not any(cell.strip() for cell in row):
            continue
        kernel_name = row[header.index('Kernel Name')].strip() if 'Kernel Name' in header else ''
        if not kernel_name:
            continue
        records.append({key: value for key, value in zip(header, row)})
    return records


def parse_name_value_metrics(path: Optional[Path]) -> Dict[str, Any]:
    rows = read_csv_matrix(path)
    if not rows:
        return {}
    header_idx = None
    metric_name_idx = None
    metric_value_idx = None
    for idx, row in enumerate(rows):
        if 'Metric Name' in row and 'Metric Value' in row:
            header_idx = idx
            metric_name_idx = row.index('Metric Name')
            metric_value_idx = row.index('Metric Value')
            break
    if header_idx is None or metric_name_idx is None or metric_value_idx is None:
        return {}
    metrics: Dict[str, Any] = {}
    for row in rows[header_idx + 1:]:
        if len(row) <= max(metric_name_idx, metric_value_idx):
            continue
        name = row[metric_name_idx].strip()
        if not name:
            continue
        metrics[name] = numeric_or_text(row[metric_value_idx])
    return metrics


def parse_generic_rows(path: Optional[Path]) -> List[Dict[str, str]]:
    lines = read_filtered_csv_lines(path)
    if not lines:
        return []
    reader = csv.DictReader(io.StringIO('\n'.join(lines)))
    if not reader.fieldnames:
        return []
    rows: List[Dict[str, str]] = []
    for raw in reader:
        row = {str(key).strip(): str(value).strip() for key, value in raw.items() if key is not None}
        if not any(value for value in row.values()):
            continue
        if is_units_row(list(row.values())):
            continue
        rows.append(row)
    return rows


def find_first(mapping: Dict[str, Any], candidates: Iterable[str]) -> Optional[str]:
    lookup = {str(key).strip().lower(): key for key in mapping.keys()}
    for candidate in candidates:
        actual = lookup.get(candidate.lower())
        if actual is None:
            continue
        value = mapping.get(actual)
        text = str(value).strip() if value is not None else ''
        if text:
            return text
    return None


def metric_direction(metric_name: str) -> str:
    lowered = metric_name.lower()
    if any(token in lowered for token in LOWER_IS_BETTER_TOKENS):
        return 'lower_better'
    if any(token in lowered for token in HIGHER_IS_BETTER_TOKENS):
        return 'higher_better'
    return 'lower_better'


def problem_score(metric_name: str, value: Optional[float]) -> float:
    if value is None:
        return 0.0
    if metric_direction(metric_name) == 'higher_better':
        return max(0.0, 100.0 - float(value))
    return max(0.0, float(value))


def metric_delta(metric_name: str, previous: Optional[float], current: Optional[float]) -> Tuple[Optional[float], str]:
    if previous is None or current is None:
        return None, 'unknown'
    delta = float(current) - float(previous)
    direction = metric_direction(metric_name)
    if abs(delta) < 1e-9:
        return delta, 'flat'
    if direction == 'higher_better':
        return delta, 'improved' if delta > 0 else 'regressed'
    return delta, 'improved' if delta < 0 else 'regressed'


def select_primary_record(records: Sequence[Dict[str, str]]) -> Optional[Dict[str, str]]:
    if not records:
        return None

    def record_key(record: Dict[str, str]) -> Tuple[float, float]:
        duration = None
        for key in (
            'gpu__time_duration.sum',
            'gpu__time_duration.avg',
            'gpu__time_duration',
            'sm__cycles_elapsed.sum',
            'sm__cycles_active.sum',
        ):
            duration = parse_float(record.get(key))
            if duration is not None:
                break
        throughput = parse_float(record.get('sm__throughput.avg.pct_of_peak_sustained_elapsed')) or 0.0
        return (duration or 0.0, throughput)

    return max(records, key=record_key)


def preferred_metric(record: Optional[Dict[str, Any]], keys: Sequence[str]) -> Any:
    if not record:
        return None
    for key in keys:
        if key in record and record.get(key) not in (None, ''):
            return numeric_or_text(record.get(key))
    return None


def build_launch(headline_record: Optional[Dict[str, Any]], raw_record: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    merged = {}
    if raw_record:
        merged.update(raw_record)
    if headline_record:
        merged.update(headline_record)
    return {
        'kernel_name': find_first(merged, ('Kernel Name', 'kernel_name')),
        'block_size': find_first(merged, ('Block Size', 'launch__block_size', 'block_size')),
        'grid_size': find_first(merged, ('Grid Size', 'launch__grid_size', 'grid_size')),
        'registers_per_thread': preferred_metric(merged, ('launch__registers_per_thread',)),
        'shared_mem_per_block_allocated': preferred_metric(
            merged,
            ('launch__shared_mem_per_block_allocated', 'launch__shared_mem_per_block', 'shared_mem_per_block_allocated'),
        ),
    }


def filter_headline_metrics(record: Optional[Dict[str, Any]], wanted_metrics: Sequence[str]) -> Dict[str, Any]:
    if not record:
        return {}
    out: Dict[str, Any] = {}
    for key in wanted_metrics:
        if key in record:
            out[key] = numeric_or_text(record[key])
    return out


def build_stall_breakdown(record: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not record:
        return []
    stalls: List[Dict[str, Any]] = []
    for metric_name, label in STALL_LABELS.items():
        value = parse_float(record.get(metric_name))
        if value is None:
            continue
        finding_id = f'stall::{label}'
        stalls.append(
            {
                'finding_id': finding_id,
                'stall_group': label,
                'metric_name': metric_name,
                'metric_value': value,
                'importance_score': value,
                'explanation': f'{label.replace("_", " ")} stalls are consuming {value:.2f}% of active warp issue slots.',
            }
        )
    stalls.sort(key=lambda item: item.get('importance_score', 0.0), reverse=True)
    return stalls


def build_memory_hierarchy(record: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        'compute_memory_throughput_pct': preferred_metric(record, ('gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed',)),
        'dram_throughput_pct': preferred_metric(record, ('dram__throughput.avg.pct_of_peak_sustained_elapsed',)),
        'lts_throughput_pct': preferred_metric(record, ('lts__throughput.avg.pct_of_peak_sustained_elapsed',)),
        'l1tex_bank_reads_pct': preferred_metric(record, ('l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed',)),
        'l1tex_bank_writes_pct': preferred_metric(record, ('l1tex__data_bank_writes.avg.pct_of_peak_sustained_elapsed',)),
    }


def build_occupancy_latency(record: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        'active_warps_pct': preferred_metric(record, ('sm__warps_active.avg.pct_of_peak_sustained_active',)),
        'occupancy_limit_registers': preferred_metric(record, ('launch__occupancy_limit_registers',)),
        'occupancy_limit_shared_mem': preferred_metric(record, ('launch__occupancy_limit_shared_mem',)),
        'occupancy_limit_blocks': preferred_metric(record, ('launch__occupancy_limit_blocks',)),
        'registers_per_thread': preferred_metric(record, ('launch__registers_per_thread',)),
        'shared_mem_per_block_allocated': preferred_metric(record, ('launch__shared_mem_per_block_allocated',)),
    }


def build_tensor_core_utilization(record: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        'tensor_pipe_active_pct': preferred_metric(record, ('sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active',)),
        'sm_throughput_pct': preferred_metric(record, ('sm__throughput.avg.pct_of_peak_sustained_elapsed',)),
        'active_warps_pct': preferred_metric(record, ('sm__warps_active.avg.pct_of_peak_sustained_active',)),
    }


def row_matches_kernel(row: Dict[str, str], kernel_name: Optional[str]) -> bool:
    if not kernel_name:
        return True
    row_kernel = find_first(row, ('Kernel Name', 'kernel_name'))
    if not row_kernel:
        return True
    return row_kernel == kernel_name


def normalize_location(row: Dict[str, str]) -> Optional[str]:
    source_file = find_first(row, ('Source File', 'File', 'Filename', 'File Name', 'source_file'))
    line = find_first(row, ('Line', 'Line Number', 'line'))
    if source_file and line:
        return f'{source_file}:{line}'
    if source_file:
        return source_file
    function_name = find_first(row, ('Function Name', 'Function', 'Device Function', 'function_name'))
    return function_name


def hotspot_scope(row: Dict[str, str]) -> Tuple[str, str, Optional[str]]:
    source_file = find_first(row, ('Source File', 'File', 'Filename', 'File Name', 'source_file'))
    line = find_first(row, ('Line', 'Line Number', 'line'))
    function_name = find_first(row, ('Function Name', 'Function', 'Device Function', 'function_name'))
    section_name = find_first(row, ('Section Name', 'Section', 'section_name'))
    if source_file:
        location = f'{source_file}:{line}' if line else source_file
        scope_name = function_name or source_file
        return 'cuda_source', scope_name, location
    if function_name:
        return 'device_function', function_name, function_name
    if section_name:
        return 'section', section_name, section_name
    return 'section', 'unknown_section', None


def build_hotspot_from_row(row: Dict[str, str], *, index: int) -> Optional[Dict[str, Any]]:
    metric_name = find_first(row, ('Metric Name', 'Metric', 'metric_name'))
    if not metric_name:
        return None
    metric_value = parse_float(find_first(row, ('Metric Value', 'Value', 'metric_value')))
    importance_override = parse_float(find_first(row, ('Importance Score', 'Importance', 'Contribution', 'importance_score')))
    metric_unit = (find_first(row, ('Metric Unit', 'Unit', 'metric_unit')) or '').strip()
    scope_type, scope_name, location = hotspot_scope(row)
    section_name = find_first(row, ('Section Name', 'Section', 'section_name'))
    lowered_metric = metric_name.lower()
    if scope_type == 'section' and lowered_metric in LOW_SIGNAL_SECTION_METRICS:
        return None
    explanation = (
        find_first(row, ('Description', 'Rule Message', 'Message', 'Advice'))
        or f'{scope_name} is carrying metric {metric_name}.'
    )
    hotspot_id = f'hotspot::{scope_type}::{slugify(scope_name)}::{slugify(location or section_name or metric_name)}::{slugify(metric_name)}'
    importance_score = importance_override
    if importance_score is None:
        importance_score = problem_score(metric_name, metric_value)
        normalized_unit = metric_unit.lower()
        if normalized_unit in RAW_TOTAL_UNITS:
            if any(token in lowered_metric for token in ('total ', 'average ', 'elapsed cycles', 'active cycles', 'threads', 'grid size')):
                importance_score = min(importance_score, 6.0)
            else:
                importance_score = min(importance_score, 15.0)
        elif normalized_unit not in PERCENT_LIKE_UNITS and metric_value is not None and abs(metric_value) > 1000:
            importance_score = min(importance_score, 15.0)
        if section_name:
            importance_score += 5.0
    return {
        'hotspot_id': hotspot_id,
        'scope_type': scope_type,
        'scope_name': scope_name,
        'location': location,
        'metric_name': metric_name,
        'metric_value': metric_value if metric_value is not None else numeric_or_text(find_first(row, ('Metric Value', 'Value', 'metric_value'))),
        'metric_unit': metric_unit or None,
        'importance_score': float(importance_score),
        'explanation': explanation,
        'section_name': section_name,
        'source_row_index': index,
    }


def dedupe_hotspots(hotspots: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_id: Dict[str, Dict[str, Any]] = {}
    for hotspot in hotspots:
        existing = by_id.get(hotspot['hotspot_id'])
        if existing is None or hotspot.get('importance_score', 0.0) > existing.get('importance_score', 0.0):
            by_id[hotspot['hotspot_id']] = hotspot
    ordered = list(by_id.values())
    ordered.sort(key=lambda item: item.get('importance_score', 0.0), reverse=True)
    return ordered


def build_fallback_hotspots(
    launch: Dict[str, Any],
    stall_breakdown: Sequence[Dict[str, Any]],
    tensor_core_utilization: Dict[str, Any],
    memory_hierarchy: Dict[str, Any],
) -> List[Dict[str, Any]]:
    hotspots: List[Dict[str, Any]] = []
    kernel_name = launch.get('kernel_name') or 'kernel'
    for stall in stall_breakdown:
        hotspots.append(
            {
                'hotspot_id': f'hotspot::section::{stall["stall_group"]}',
                'scope_type': 'section',
                'scope_name': f'stall_{stall["stall_group"]}',
                'location': kernel_name,
                'metric_name': stall['metric_name'],
                'metric_value': stall['metric_value'],
                'importance_score': stall['importance_score'],
                'explanation': stall['explanation'],
                'section_name': 'Scheduler',
            }
        )
    tensor_pct = parse_float(tensor_core_utilization.get('tensor_pipe_active_pct'))
    if tensor_pct is not None:
        hotspots.append(
            {
                'hotspot_id': 'hotspot::section::tensor_pipe_activity',
                'scope_type': 'section',
                'scope_name': 'tensor_pipe_activity',
                'location': kernel_name,
                'metric_name': 'sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active',
                'metric_value': tensor_pct,
                'importance_score': problem_score('sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active', tensor_pct),
                'explanation': f'Tensor pipe activity is only {tensor_pct:.2f}% of peak sustained active on the dominant kernel.',
                'section_name': 'Compute',
            }
        )
    dram_pct = parse_float(memory_hierarchy.get('dram_throughput_pct'))
    if dram_pct is not None:
        hotspots.append(
            {
                'hotspot_id': 'hotspot::section::dram_throughput',
                'scope_type': 'section',
                'scope_name': 'dram_throughput',
                'location': kernel_name,
                'metric_name': 'dram__throughput.avg.pct_of_peak_sustained_elapsed',
                'metric_value': dram_pct,
                'importance_score': dram_pct,
                'explanation': f'DRAM throughput is {dram_pct:.2f}% of peak sustained elapsed on the dominant kernel.',
                'section_name': 'Memory',
            }
        )
    return dedupe_hotspots(hotspots)


def build_rules(rows: Sequence[Dict[str, str]], kernel_name: Optional[str]) -> List[Dict[str, Any]]:
    rules: List[Dict[str, Any]] = []
    seen: set[str] = set()
    for idx, row in enumerate(rows):
        if not row_matches_kernel(row, kernel_name):
            continue
        rule_name = find_first(row, ('Rule Name', 'Rule', 'rule_name'))
        if not rule_name:
            continue
        section_name = find_first(row, ('Section Name', 'Section', 'section_name'))
        metric_name = find_first(row, ('Metric Name', 'Metric', 'metric_name'))
        metric_value = parse_float(find_first(row, ('Metric Value', 'Value', 'metric_value')))
        severity = (find_first(row, ('Severity', 'Rule Severity', 'severity')) or 'info').lower()
        message = find_first(row, ('Rule Message', 'Message', 'Advice', 'Description')) or rule_name
        rule_id = f'rule::{slugify(rule_name)}::{idx}'
        if rule_id in seen:
            continue
        seen.add(rule_id)
        rules.append(
            {
                'rule_id': rule_id,
                'rule_name': rule_name,
                'severity': severity,
                'section_name': section_name,
                'metric_name': metric_name,
                'metric_value': metric_value if metric_value is not None else numeric_or_text(find_first(row, ('Metric Value', 'Value', 'metric_value'))),
                'message': message,
                'location': normalize_location(row),
                'importance_score': problem_score(metric_name or rule_name, metric_value) + {'error': 25.0, 'warning': 15.0, 'info': 5.0}.get(severity, 0.0),
            }
        )
    rules.sort(key=lambda item: item.get('importance_score', 0.0), reverse=True)
    return rules


def build_section_highlights(
    hotspots: Sequence[Dict[str, Any]],
    rules: Sequence[Dict[str, Any]],
    stall_breakdown: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = {}
    for hotspot in hotspots:
        section_name = hotspot.get('section_name') or hotspot.get('scope_name') or 'unknown_section'
        current = grouped.get(section_name)
        if current is None or hotspot.get('importance_score', 0.0) > current.get('importance_score', 0.0):
            grouped[section_name] = {
                'section_id': f'section::{slugify(section_name)}',
                'section_name': section_name,
                'metric_name': hotspot.get('metric_name'),
                'metric_value': hotspot.get('metric_value'),
                'importance_score': hotspot.get('importance_score', 0.0),
                'summary': hotspot.get('explanation'),
                'rule_ids': [],
                'hotspot_ids': [hotspot.get('hotspot_id')],
            }
    for rule in rules:
        section_name = rule.get('section_name') or 'rule_only'
        current = grouped.get(section_name)
        if current is None:
            grouped[section_name] = {
                'section_id': f'section::{slugify(section_name)}',
                'section_name': section_name,
                'metric_name': rule.get('metric_name'),
                'metric_value': rule.get('metric_value'),
                'importance_score': rule.get('importance_score', 0.0),
                'summary': rule.get('message'),
                'rule_ids': [rule.get('rule_id')],
                'hotspot_ids': [],
            }
        else:
            current.setdefault('rule_ids', []).append(rule.get('rule_id'))
            if rule.get('importance_score', 0.0) > current.get('importance_score', 0.0):
                current['metric_name'] = rule.get('metric_name')
                current['metric_value'] = rule.get('metric_value')
                current['importance_score'] = rule.get('importance_score', 0.0)
                current['summary'] = rule.get('message')
    if stall_breakdown:
        top_stall = stall_breakdown[0]
        grouped.setdefault(
            'Scheduler',
            {
                'section_id': 'section::scheduler',
                'section_name': 'Scheduler',
                'metric_name': top_stall.get('metric_name'),
                'metric_value': top_stall.get('metric_value'),
                'importance_score': top_stall.get('importance_score', 0.0),
                'summary': top_stall.get('explanation'),
                'rule_ids': [],
                'hotspot_ids': [],
            },
        )
    highlights = list(grouped.values())
    highlights.sort(key=lambda item: item.get('importance_score', 0.0), reverse=True)
    return highlights


def metric_ref(kind: str, ref_id: str, metric_name: str, metric_value: Any, summary: str) -> Dict[str, Any]:
    return {
        'kind': kind,
        'ref_id': ref_id,
        'metric_name': metric_name,
        'metric_value': metric_value,
        'summary': summary,
    }


def add_bottleneck(
    items: List[Dict[str, Any]],
    *,
    class_id: str,
    severity_score: float,
    summary: str,
    evidence: Sequence[Dict[str, Any]],
) -> None:
    if severity_score <= 0 or not evidence:
        return
    items.append(
        {
            'class_id': class_id,
            'severity_score': round(float(severity_score), 4),
            'summary': summary,
            'evidence': list(evidence),
        }
    )


def metric_display(value: Optional[float], suffix: str = '') -> str:
    if value is None:
        return 'N/A'
    return f'{value:.2f}{suffix}'


def classify_bottlenecks(
    launch: Dict[str, Any],
    stall_breakdown: Sequence[Dict[str, Any]],
    memory_hierarchy: Dict[str, Any],
    occupancy_latency: Dict[str, Any],
    tensor_core_utilization: Dict[str, Any],
    rules: Sequence[Dict[str, Any]],
    section_highlights: Sequence[Dict[str, Any]],
    hotspots: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    classes: List[Dict[str, Any]] = []
    tensor_pct = parse_float(tensor_core_utilization.get('tensor_pipe_active_pct'))
    sm_pct = parse_float(tensor_core_utilization.get('sm_throughput_pct'))
    active_warps = parse_float(occupancy_latency.get('active_warps_pct'))
    dram_pct = parse_float(memory_hierarchy.get('dram_throughput_pct'))
    lts_pct = parse_float(memory_hierarchy.get('lts_throughput_pct'))
    compute_mem_pct = parse_float(memory_hierarchy.get('compute_memory_throughput_pct'))
    regs_per_thread = parse_float(occupancy_latency.get('registers_per_thread'))
    occ_reg_limit = parse_float(occupancy_latency.get('occupancy_limit_registers'))
    occ_shared_limit = parse_float(occupancy_latency.get('occupancy_limit_shared_mem'))
    l1_bank_reads = parse_float(memory_hierarchy.get('l1tex_bank_reads_pct'))
    l1_bank_writes = parse_float(memory_hierarchy.get('l1tex_bank_writes_pct'))

    stalls_by_name = {stall['stall_group']: stall for stall in stall_breakdown}
    top_hotspots = hotspots[:3]
    hotspot_text = ' '.join(
        str(hotspot.get('scope_name') or '') + ' ' + str(hotspot.get('explanation') or '')
        for hotspot in hotspots[:6]
    ).lower()
    rule_text = ' '.join(
        str(rule.get('rule_name') or '') + ' ' + str(rule.get('message') or '')
        for rule in rules[:10]
    ).lower()

    tensor_evidence: List[Dict[str, Any]] = []
    tensor_problem = 0.0
    if tensor_pct is not None and tensor_pct < 65.0:
        tensor_problem += (65.0 - tensor_pct)
        tensor_evidence.append(
            metric_ref(
                'headline_metric',
                'metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active',
                'sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active',
                tensor_pct,
                f'Tensor pipe activity is only {tensor_pct:.2f}% of peak sustained active.',
            )
        )
    if active_warps is not None and active_warps < 30.0:
        tensor_problem += (30.0 - active_warps) * 0.8
        tensor_evidence.append(
            metric_ref(
                'headline_metric',
                'metric::sm__warps_active.avg.pct_of_peak_sustained_active',
                'sm__warps_active.avg.pct_of_peak_sustained_active',
                active_warps,
                f'Active warps are only {active_warps:.2f}% of peak sustained active.',
            )
        )
    if dram_pct is not None and dram_pct < 45.0:
        tensor_problem += 5.0
    if top_hotspots:
        tensor_evidence.append(
            metric_ref(
                'source_hotspot',
                top_hotspots[0]['hotspot_id'],
                top_hotspots[0]['metric_name'],
                top_hotspots[0]['metric_value'],
                top_hotspots[0]['explanation'],
            )
        )
    add_bottleneck(
        classes,
        class_id='tensor_core_underutilization',
        severity_score=tensor_problem,
        summary=(
            f'Tensor activity ({metric_display(tensor_pct, "%")}) is low relative to available memory bandwidth, '
            f'and active warps ({metric_display(active_warps, "%")}) are not hiding latency.'
        ),
        evidence=tensor_evidence,
    )

    memory_evidence: List[Dict[str, Any]] = []
    memory_problem = 0.0
    if compute_mem_pct is not None and compute_mem_pct > 60.0:
        memory_problem += compute_mem_pct - 60.0
        memory_evidence.append(
            metric_ref(
                'headline_metric',
                'metric::gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed',
                'gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed',
                compute_mem_pct,
                f'Compute-memory throughput is {compute_mem_pct:.2f}% of peak sustained elapsed.',
            )
        )
    if dram_pct is not None and dram_pct > 55.0:
        memory_problem += dram_pct - 55.0
        memory_evidence.append(
            metric_ref(
                'headline_metric',
                'metric::dram__throughput.avg.pct_of_peak_sustained_elapsed',
                'dram__throughput.avg.pct_of_peak_sustained_elapsed',
                dram_pct,
                f'DRAM throughput is {dram_pct:.2f}% of peak sustained elapsed.',
            )
        )
    if lts_pct is not None and lts_pct > 45.0:
        memory_problem += lts_pct - 45.0
    if 'memory' in rule_text:
        memory_problem += 8.0
        if rules:
            memory_evidence.append(
                metric_ref(
                    'rule',
                    rules[0]['rule_id'],
                    rules[0].get('metric_name') or rules[0]['rule_name'],
                    rules[0].get('metric_value'),
                    rules[0].get('message'),
                )
            )
    add_bottleneck(
        classes,
        class_id='global_memory_bound',
        severity_score=memory_problem,
        summary='Memory throughput and memory-focused sections/rules suggest the dominant kernel is being limited by global or cache movement.',
        evidence=memory_evidence,
    )

    shared_evidence: List[Dict[str, Any]] = []
    shared_problem = 0.0
    if l1_bank_reads is not None and l1_bank_reads > 8.0:
        shared_problem += l1_bank_reads - 8.0
        shared_evidence.append(
            metric_ref(
                'headline_metric',
                'metric::l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed',
                'l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed',
                l1_bank_reads,
                f'L1/shared bank read activity is {l1_bank_reads:.2f}% of peak sustained elapsed.',
            )
        )
    if l1_bank_writes is not None and l1_bank_writes > 4.0:
        shared_problem += (l1_bank_writes - 4.0) * 1.5
        shared_evidence.append(
            metric_ref(
                'headline_metric',
                'metric::l1tex__data_bank_writes.avg.pct_of_peak_sustained_elapsed',
                'l1tex__data_bank_writes.avg.pct_of_peak_sustained_elapsed',
                l1_bank_writes,
                f'L1/shared bank write activity is {l1_bank_writes:.2f}% of peak sustained elapsed.',
            )
        )
    shared_hotspots = [hotspot for hotspot in hotspots if 'bank' in str(hotspot.get('metric_name') or '').lower()]
    if shared_hotspots:
        shared_problem += 10.0
        shared_evidence.append(
            metric_ref(
                'source_hotspot',
                shared_hotspots[0]['hotspot_id'],
                shared_hotspots[0]['metric_name'],
                shared_hotspots[0]['metric_value'],
                shared_hotspots[0]['explanation'],
            )
        )
    add_bottleneck(
        classes,
        class_id='shared_memory_bottleneck',
        severity_score=shared_problem,
        summary='Shared-memory bank activity or hotspot evidence suggests the hot path is paying extra shared-memory cost.',
        evidence=shared_evidence,
    )

    occupancy_evidence: List[Dict[str, Any]] = []
    occupancy_problem = 0.0
    if active_warps is not None and active_warps < 25.0:
        occupancy_problem += 25.0 - active_warps
        occupancy_evidence.append(
            metric_ref(
                'headline_metric',
                'metric::sm__warps_active.avg.pct_of_peak_sustained_active',
                'sm__warps_active.avg.pct_of_peak_sustained_active',
                active_warps,
                f'Active warps are only {active_warps:.2f}% of peak sustained active.',
            )
        )
    if occ_reg_limit is not None and occ_reg_limit <= 2.0:
        occupancy_problem += 12.0
        occupancy_evidence.append(
            metric_ref(
                'headline_metric',
                'metric::launch__occupancy_limit_registers',
                'launch__occupancy_limit_registers',
                occ_reg_limit,
                f'Register pressure is limiting occupancy to {occ_reg_limit:.0f} blocks per SM.',
            )
        )
    if occ_shared_limit is not None and occ_shared_limit <= 2.0:
        occupancy_problem += 8.0
        occupancy_evidence.append(
            metric_ref(
                'headline_metric',
                'metric::launch__occupancy_limit_shared_mem',
                'launch__occupancy_limit_shared_mem',
                occ_shared_limit,
                f'Shared-memory footprint is limiting occupancy to {occ_shared_limit:.0f} blocks per SM.',
            )
        )
    if regs_per_thread is not None and regs_per_thread >= 128.0:
        occupancy_problem += min(20.0, (regs_per_thread - 128.0) * 0.2)
    add_bottleneck(
        classes,
        class_id='occupancy_latency_hiding_issue',
        severity_score=occupancy_problem,
        summary='Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.',
        evidence=occupancy_evidence,
    )

    barrier = stalls_by_name.get('barrier')
    barrier_evidence: List[Dict[str, Any]] = []
    barrier_problem = 0.0
    if barrier is not None:
        barrier_problem += barrier.get('metric_value', 0.0)
        barrier_evidence.append(
            metric_ref(
                'stall_breakdown',
                barrier['finding_id'],
                barrier['metric_name'],
                barrier['metric_value'],
                barrier['explanation'],
            )
        )
    if 'sync' in hotspot_text or 'barrier' in hotspot_text or 'barrier' in rule_text:
        barrier_problem += 8.0
    add_bottleneck(
        classes,
        class_id='synchronization_barrier_issue',
        severity_score=barrier_problem,
        summary='Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.',
        evidence=barrier_evidence,
    )

    generic_evidence: List[Dict[str, Any]] = []
    generic_problem = 0.0
    if any(token in hotspot_text for token in ('tail', 'epilogue', 'predicate', 'cleanup', 'generic')):
        generic_problem += 15.0
    if any(token in rule_text for token in ('tail', 'epilogue', 'predicate', 'cleanup', 'generic')):
        generic_problem += 12.0
    if section_highlights:
        generic_section = next(
            (
                highlight
                for highlight in section_highlights
                if any(token in str(highlight.get('summary') or '').lower() for token in ('tail', 'epilogue', 'predicate', 'cleanup', 'generic'))
            ),
            None,
        )
        if generic_section is not None:
            generic_evidence.append(
                metric_ref(
                    'section_highlight',
                    generic_section['section_id'],
                    generic_section.get('metric_name') or generic_section['section_name'],
                    generic_section.get('metric_value'),
                    generic_section.get('summary'),
                )
            )
    add_bottleneck(
        classes,
        class_id='tail_overhead_or_generic_path_issue',
        severity_score=generic_problem,
        summary='Tail or generic-path evidence suggests some of the runtime is being spent in cleanup or non-steady-state work.',
        evidence=generic_evidence,
    )

    classes.sort(key=lambda item: item.get('severity_score', 0.0), reverse=True)
    for idx, item in enumerate(classes, start=1):
        item['rank'] = idx
    return classes


def compact_bottleneck_class(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'class_id': item.get('class_id'),
        'rank': item.get('rank'),
        'severity_score': item.get('severity_score'),
        'summary': item.get('summary'),
        'evidence': item.get('evidence', [])[:3],
    }


def top_hotspot_deltas(delta_summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    buckets = []
    source_hotspots = delta_summary.get('source_hotspots') or {}
    for bucket_name in ('regressed', 'new', 'improved', 'disappeared'):
        for item in source_hotspots.get(bucket_name, []):
            enriched = dict(item)
            enriched['bucket'] = bucket_name
            buckets.append(enriched)
    buckets.sort(key=hotspot_delta_rank_score, reverse=True)
    return buckets[:TOP_HOTSPOT_LIMIT]


def hotspot_delta_rank_score(item: Dict[str, Any]) -> float:
    delta = abs(parse_float(item.get('delta')) or 0.0)
    importance = min(float(item.get('importance_score') or 0.0), 25.0)
    bucket = str(item.get('bucket') or '')
    if delta > 0:
        return delta + importance
    if bucket in {'new', 'disappeared'}:
        return min(importance, 10.0)
    return importance


def build_top_findings(
    bottlenecks: Sequence[Dict[str, Any]],
    hotspots: Sequence[Dict[str, Any]],
    delta_summary: Dict[str, Any],
) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    for item in bottlenecks[:4]:
        evidence = item.get('evidence', [])
        findings.append(
            {
                'finding_id': f'finding::{item.get("class_id")}',
                'finding_type': 'bottleneck_class',
                'summary': item.get('summary'),
                'importance_score': item.get('severity_score'),
                'evidence': evidence,
            }
        )
    for hotspot in hotspots[:2]:
        findings.append(
            {
                'finding_id': f'finding::{hotspot.get("hotspot_id")}',
                'finding_type': 'source_hotspot',
                'summary': hotspot.get('explanation'),
                'importance_score': hotspot.get('importance_score'),
                'evidence': [
                    metric_ref(
                        'source_hotspot',
                        hotspot.get('hotspot_id'),
                        hotspot.get('metric_name'),
                        hotspot.get('metric_value'),
                        hotspot.get('explanation'),
                    )
                ],
            }
        )
    for delta_item in top_hotspot_deltas(delta_summary)[:2]:
        findings.append(
            {
                'finding_id': f'finding::delta::{delta_item.get("hotspot_id")}',
                'finding_type': 'hotspot_delta',
                'summary': f'{delta_item.get("bucket")} hotspot delta at {delta_item.get("scope_name") or delta_item.get("location")}: {delta_item.get("trend", "changed")}.',
                'importance_score': hotspot_delta_rank_score(delta_item),
                'evidence': [delta_item],
            }
        )
    findings.sort(key=lambda item: item.get('importance_score') or 0.0, reverse=True)
    deduped: List[Dict[str, Any]] = []
    seen: set[str] = set()
    for finding in findings:
        finding_id = str(finding.get('finding_id'))
        if finding_id in seen:
            continue
        seen.add(finding_id)
        deduped.append(finding)
    return deduped[:TOP_FINDING_LIMIT]


def build_node_b_handoff(
    bottlenecks: Sequence[Dict[str, Any]],
    hotspots: Sequence[Dict[str, Any]],
    rules: Sequence[Dict[str, Any]],
    delta_summary: Dict[str, Any],
) -> Dict[str, Any]:
    top_findings = build_top_findings(bottlenecks, hotspots, delta_summary)
    code_regions = []
    seen_regions: set[str] = set()
    for hotspot in hotspots[:TOP_HOTSPOT_LIMIT]:
        region_key = str(hotspot.get('location') or hotspot.get('scope_name'))
        if not region_key or region_key in seen_regions:
            continue
        seen_regions.add(region_key)
        code_regions.append(
            {
                'region_id': hotspot.get('hotspot_id'),
                'scope_type': hotspot.get('scope_type'),
                'scope_name': hotspot.get('scope_name'),
                'location': hotspot.get('location'),
                'reason': hotspot.get('explanation'),
            }
        )
    for rule in rules[:3]:
        region_key = str(rule.get('location') or rule.get('rule_name'))
        if not region_key or region_key in seen_regions:
            continue
        seen_regions.add(region_key)
        code_regions.append(
            {
                'region_id': rule.get('rule_id'),
                'scope_type': 'rule',
                'scope_name': rule.get('rule_name'),
                'location': rule.get('location'),
                'reason': rule.get('message'),
            }
        )
    return {
        'top_findings': top_findings,
        'code_regions_to_investigate': code_regions[:TOP_HOTSPOT_LIMIT],
    }


def build_guardrail_metrics(
    headline_metrics: Dict[str, Any],
    bottlenecks: Sequence[Dict[str, Any]],
    stall_breakdown: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    guardrails: List[Dict[str, Any]] = []
    tensor_metric = 'sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active'
    tensor_value = parse_float(headline_metrics.get(tensor_metric))
    if tensor_value is not None:
        guardrails.append(
            {
                'metric_name': tensor_metric,
                'current_value': tensor_value,
                'guardrail': 'non_decreasing',
                'reason': 'Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.',
            }
        )
    active_warps_metric = 'sm__warps_active.avg.pct_of_peak_sustained_active'
    active_warps_value = parse_float(headline_metrics.get(active_warps_metric))
    if active_warps_value is not None:
        guardrails.append(
            {
                'metric_name': active_warps_metric,
                'current_value': active_warps_value,
                'guardrail': 'non_decreasing',
                'reason': 'Latency-hiding is already weak; active warps should not regress.',
            }
        )
    for stall in stall_breakdown[:2]:
        guardrails.append(
            {
                'metric_name': stall.get('metric_name'),
                'current_value': stall.get('metric_value'),
                'guardrail': 'non_increasing',
                'reason': stall.get('explanation'),
            }
        )
    return guardrails[:4]


def build_node_c_handoff(
    headline_metrics: Dict[str, Any],
    bottlenecks: Sequence[Dict[str, Any]],
    hotspots: Sequence[Dict[str, Any]],
    stall_breakdown: Sequence[Dict[str, Any]],
    delta_summary: Dict[str, Any],
) -> Dict[str, Any]:
    expected_recheck_points = []
    for hotspot in hotspots[:4]:
        expected_recheck_points.append(
            {
                'scope_type': hotspot.get('scope_type'),
                'scope_name': hotspot.get('scope_name'),
                'location': hotspot.get('location'),
                'metric_name': hotspot.get('metric_name'),
                'reason': hotspot.get('explanation'),
            }
        )
    for delta_item in top_hotspot_deltas(delta_summary)[:2]:
        expected_recheck_points.append(
            {
                'scope_type': delta_item.get('scope_type'),
                'scope_name': delta_item.get('scope_name'),
                'location': delta_item.get('location'),
                'metric_name': delta_item.get('metric_name'),
                'reason': f'Previous delta was {delta_item.get("trend", "changed")} in the {delta_item.get("bucket")} bucket.',
            }
        )
    return {
        'target_hotspots': list(hotspots[:TOP_HOTSPOT_LIMIT]),
        'guardrail_metrics': build_guardrail_metrics(headline_metrics, bottlenecks, stall_breakdown),
        'expected_recheck_points': expected_recheck_points[:TOP_HOTSPOT_LIMIT],
    }


def summarize_delta_metrics(
    previous_metrics: Dict[str, Any],
    current_metrics: Dict[str, Any],
) -> Dict[str, Dict[str, Any]]:
    all_keys = sorted(set(previous_metrics.keys()) | set(current_metrics.keys()))
    delta_summary: Dict[str, Dict[str, Any]] = {}
    for metric_name in all_keys:
        previous_value = parse_float(previous_metrics.get(metric_name))
        current_value = parse_float(current_metrics.get(metric_name))
        delta, trend = metric_delta(metric_name, previous_value, current_value)
        delta_summary[metric_name] = {
            'previous': previous_metrics.get(metric_name),
            'current': current_metrics.get(metric_name),
            'delta': delta,
            'trend': trend,
        }
    return delta_summary


def summarize_stall_deltas(
    previous_stalls: Sequence[Dict[str, Any]],
    current_stalls: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    by_id = {stall.get('stall_group'): stall for stall in previous_stalls}
    deltas: List[Dict[str, Any]] = []
    for stall in current_stalls:
        group = stall.get('stall_group')
        previous_value = parse_float((by_id.get(group) or {}).get('metric_value'))
        current_value = parse_float(stall.get('metric_value'))
        delta, trend = metric_delta(stall.get('metric_name'), previous_value, current_value)
        deltas.append(
            {
                'stall_group': group,
                'metric_name': stall.get('metric_name'),
                'previous': previous_value,
                'current': current_value,
                'delta': delta,
                'trend': trend,
            }
        )
    deltas.sort(key=lambda item: abs(item.get('delta') or 0.0), reverse=True)
    return deltas


def hotspot_delta_entry(previous: Dict[str, Any], current: Dict[str, Any]) -> Dict[str, Any]:
    previous_value = parse_float(previous.get('metric_value'))
    current_value = parse_float(current.get('metric_value'))
    delta, trend = metric_delta(str(current.get('metric_name') or previous.get('metric_name') or ''), previous_value, current_value)
    return {
        'hotspot_id': current.get('hotspot_id') or previous.get('hotspot_id'),
        'scope_type': current.get('scope_type') or previous.get('scope_type'),
        'scope_name': current.get('scope_name') or previous.get('scope_name'),
        'location': current.get('location') or previous.get('location'),
        'metric_name': current.get('metric_name') or previous.get('metric_name'),
        'previous': previous_value,
        'current': current_value,
        'delta': delta,
        'trend': trend,
        'importance_score': max(current.get('importance_score') or 0.0, previous.get('importance_score') or 0.0),
        'explanation': current.get('explanation') or previous.get('explanation'),
    }


def compute_delta_vs_previous_run(
    previous_analysis: Optional[Dict[str, Any]],
    current_analysis: Dict[str, Any],
) -> Dict[str, Any]:
    if not previous_analysis:
        return {
            'baseline_run_id': None,
            'headline_metrics': {},
            'stall_breakdown': [],
            'source_hotspots': {
                'improved': [],
                'regressed': [],
                'new': [],
                'disappeared': [],
            },
        }

    current_hotspots = {item.get('hotspot_id'): item for item in current_analysis.get('source_hotspots', [])}
    previous_hotspots = {item.get('hotspot_id'): item for item in previous_analysis.get('source_hotspots', [])}
    improved: List[Dict[str, Any]] = []
    regressed: List[Dict[str, Any]] = []
    new: List[Dict[str, Any]] = []
    disappeared: List[Dict[str, Any]] = []

    for hotspot_id, current in current_hotspots.items():
        previous = previous_hotspots.get(hotspot_id)
        if previous is None:
            entry = dict(current)
            entry['trend'] = 'new'
            new.append(entry)
            continue
        delta_entry = hotspot_delta_entry(previous, current)
        if delta_entry.get('trend') == 'improved':
            improved.append(delta_entry)
        elif delta_entry.get('trend') == 'regressed':
            regressed.append(delta_entry)

    for hotspot_id, previous in previous_hotspots.items():
        if hotspot_id not in current_hotspots:
            entry = dict(previous)
            entry['trend'] = 'disappeared'
            disappeared.append(entry)

    for bucket in (improved, regressed, new, disappeared):
        bucket.sort(key=lambda item: abs(parse_float(item.get('delta')) or item.get('importance_score') or 0.0), reverse=True)

    return {
        'baseline_run_id': previous_analysis.get('source_run_id'),
        'headline_metrics': summarize_delta_metrics(
            previous_analysis.get('headline_metrics') or {},
            current_analysis.get('headline_metrics') or {},
        ),
        'stall_breakdown': summarize_stall_deltas(
            previous_analysis.get('stall_breakdown') or [],
            current_analysis.get('stall_breakdown') or [],
        ),
        'source_hotspots': {
            'improved': improved[:TOP_HOTSPOT_LIMIT],
            'regressed': regressed[:TOP_HOTSPOT_LIMIT],
            'new': new[:TOP_HOTSPOT_LIMIT],
            'disappeared': disappeared[:TOP_HOTSPOT_LIMIT],
        },
    }


def compress_delta_for_summary(delta_summary: Dict[str, Any]) -> Dict[str, Any]:
    headline_items = sorted(
        delta_summary.get('headline_metrics', {}).items(),
        key=lambda item: abs((item[1] or {}).get('delta') or 0.0),
        reverse=True,
    )
    headline_compact = {name: payload for name, payload in headline_items[:8]}
    return {
        'baseline_run_id': delta_summary.get('baseline_run_id'),
        'headline_metrics': headline_compact,
        'stall_breakdown': list((delta_summary.get('stall_breakdown') or [])[:6]),
        'source_hotspots': {
            key: list((delta_summary.get('source_hotspots') or {}).get(key, [])[:4])
            for key in ('improved', 'regressed', 'new', 'disappeared')
        },
    }


def read_unavailable_reason(log_path: Optional[Path], fallback: str) -> str:
    if log_path and log_path.exists():
        lines = [line.strip() for line in log_path.read_text(encoding='utf-8', errors='replace').splitlines() if line.strip()]
        if lines:
            return lines[-1]
    return fallback


def artifact_entry(
    *,
    kind: str,
    path: Optional[Path],
    base_dir: Optional[Path],
    status: str,
    return_code: Optional[int] = None,
    unavailable_reason: Optional[str] = None,
    best_effort: bool = False,
    legacy_alias: Optional[Path] = None,
) -> Dict[str, Any]:
    payload = {
        'artifact_kind': kind,
        'path': _relativize_path(path, base_dir),
        'status': status,
        'return_code': return_code,
        'best_effort': best_effort,
    }
    if unavailable_reason:
        payload['unavailable_reason'] = unavailable_reason
    if legacy_alias:
        payload['legacy_alias_path'] = _relativize_path(legacy_alias, base_dir)
    return payload


def default_artifacts(
    *,
    run_dir: Path,
    rep_path: Optional[Path],
    headline_csv_path: Optional[Path],
    import_raw_path: Optional[Path],
    details_page_path: Optional[Path],
    source_csv_path: Optional[Path],
    legacy_import_raw_alias: Optional[Path],
    source_unavailable_reason: Optional[str],
    details_unavailable_reason: Optional[str],
    import_raw_unavailable_reason: Optional[str],
    source_structured_hotspots_available: bool = True,
    return_codes: Optional[Dict[str, Optional[int]]] = None,
) -> Dict[str, Any]:
    return_codes = return_codes or {}
    base_dir = run_dir.parent
    artifacts = {
        'ncu_rep': artifact_entry(
            kind='report',
            path=rep_path,
            base_dir=base_dir,
            status='available' if rep_path and rep_path.exists() else 'missing',
            return_code=return_codes.get('rep'),
        ),
        'headline_csv': artifact_entry(
            kind='headline_raw_page',
            path=headline_csv_path,
            base_dir=base_dir,
            status='available' if headline_csv_path and headline_csv_path.exists() else 'missing',
            return_code=return_codes.get('headline_csv'),
        ),
        'import_raw_page': artifact_entry(
            kind='import_raw_page',
            path=import_raw_path,
            base_dir=base_dir,
            status='available' if import_raw_path and import_raw_path.exists() else 'unavailable',
            return_code=return_codes.get('import_raw'),
            unavailable_reason=import_raw_unavailable_reason,
            legacy_alias=legacy_import_raw_alias,
        ),
        'details_page': artifact_entry(
            kind='details_page',
            path=details_page_path,
            base_dir=base_dir,
            status='available' if details_page_path and details_page_path.exists() else 'unavailable',
            return_code=return_codes.get('details_page'),
            unavailable_reason=details_unavailable_reason,
            best_effort=False,
        ),
        'source_page': artifact_entry(
            kind='source_page',
            path=source_csv_path,
            base_dir=base_dir,
            status='available' if source_csv_path and source_csv_path.exists() else 'unavailable',
            return_code=return_codes.get('source_page'),
            unavailable_reason=source_unavailable_reason,
            best_effort=True,
        ),
    }
    source_page = artifacts['source_page']
    source_page['structured_hotspots_available'] = bool(source_structured_hotspots_available)
    return artifacts


def analyze_run(
    *,
    run_dir: Path,
    source_run_id: str,
    headline_csv_path: Optional[Path],
    import_raw_path: Optional[Path],
    details_page_path: Optional[Path],
    source_csv_path: Optional[Path],
    rep_path: Optional[Path],
    wanted_headline_metrics: Sequence[str],
    previous_analysis_path: Optional[Path] = None,
    source_unavailable_reason: Optional[str] = None,
    details_unavailable_reason: Optional[str] = None,
    import_raw_unavailable_reason: Optional[str] = None,
    legacy_import_raw_alias: Optional[Path] = None,
    return_codes: Optional[Dict[str, Optional[int]]] = None,
) -> Dict[str, Any]:
    headline_records = parse_wide_csv_records(headline_csv_path)
    import_raw_records = parse_wide_csv_records(import_raw_path)
    details_rows = parse_generic_rows(details_page_path)
    source_rows = parse_generic_rows(source_csv_path)
    headline_metrics_kv = parse_name_value_metrics(headline_csv_path)
    source_export_is_disassembly = source_page_is_disassembly(source_csv_path)

    primary_headline = select_primary_record(headline_records) or (headline_records[0] if headline_records else None)
    primary_raw = select_primary_record(import_raw_records) or primary_headline
    launch = build_launch(primary_headline, primary_raw)
    kernel_name = launch.get('kernel_name')

    headline_metrics = filter_headline_metrics(primary_headline, wanted_headline_metrics)
    if not headline_metrics:
        headline_metrics = {key: value for key, value in headline_metrics_kv.items() if key in wanted_headline_metrics}

    filtered_details = [row for row in details_rows if row_matches_kernel(row, kernel_name)]
    filtered_source = [row for row in source_rows if row_matches_kernel(row, kernel_name)]
    source_structured_hotspots_available = bool(filtered_source)
    if source_csv_path and source_csv_path.exists() and not source_structured_hotspots_available:
        if source_export_is_disassembly:
            source_unavailable_reason = (
                source_unavailable_reason
                or 'source export resolved to SASS/disassembly without correlated metric rows; falling back to details/section findings'
            )
        else:
            source_unavailable_reason = (
                source_unavailable_reason
                or 'source export did not contain structured metric rows for the dominant kernel; falling back to details/section findings'
            )

    stall_breakdown = build_stall_breakdown(primary_headline or primary_raw)
    memory_hierarchy = build_memory_hierarchy(primary_headline or primary_raw)
    occupancy_latency = build_occupancy_latency(primary_headline or primary_raw)
    tensor_core_utilization = build_tensor_core_utilization(primary_headline or primary_raw)
    rules = build_rules(filtered_details, kernel_name)
    hotspot_rows = filtered_source if filtered_source else filtered_details
    hotspots = dedupe_hotspots(
        [
            hotspot
            for idx, row in enumerate(hotspot_rows)
            for hotspot in ([build_hotspot_from_row(row, index=idx)] if build_hotspot_from_row(row, index=idx) else [])
        ]
    )
    if not hotspots:
        hotspots = build_fallback_hotspots(launch, stall_breakdown, tensor_core_utilization, memory_hierarchy)
    section_highlights = build_section_highlights(hotspots, rules, stall_breakdown)
    artifacts = default_artifacts(
        run_dir=run_dir,
        rep_path=rep_path,
        headline_csv_path=headline_csv_path,
        import_raw_path=import_raw_path,
        details_page_path=details_page_path,
        source_csv_path=source_csv_path,
        legacy_import_raw_alias=legacy_import_raw_alias,
        source_unavailable_reason=source_unavailable_reason,
        details_unavailable_reason=details_unavailable_reason,
        import_raw_unavailable_reason=import_raw_unavailable_reason,
        source_structured_hotspots_available=source_structured_hotspots_available,
        return_codes=return_codes,
    )

    provisional_analysis = {
        'schema_version': SCHEMA_VERSION,
        'status': 'available' if (primary_headline or primary_raw) else 'missing',
        'source_run_id': source_run_id,
        'source_run_dir': _relativize_path(run_dir, run_dir.parent),
        'launch': launch,
        'headline_metrics': headline_metrics,
        'stall_breakdown': stall_breakdown,
        'memory_hierarchy': memory_hierarchy,
        'occupancy_latency': occupancy_latency,
        'tensor_core_utilization': tensor_core_utilization,
        'rules': rules,
        'section_highlights': section_highlights,
        'source_hotspots': hotspots[:TOP_HOTSPOT_LIMIT],
        'artifacts': artifacts,
    }

    previous_analysis = None
    if previous_analysis_path and previous_analysis_path.exists():
        previous_analysis = load_json(previous_analysis_path)
    bottleneck_classes = classify_bottlenecks(
        launch,
        stall_breakdown,
        memory_hierarchy,
        occupancy_latency,
        tensor_core_utilization,
        rules,
        section_highlights,
        hotspots,
    )
    provisional_analysis['bottleneck_classes'] = bottleneck_classes
    provisional_analysis['delta_vs_previous_run'] = compute_delta_vs_previous_run(previous_analysis, provisional_analysis)
    provisional_analysis['handoff'] = {
        'node_b': build_node_b_handoff(
            bottleneck_classes,
            hotspots,
            rules,
            provisional_analysis['delta_vs_previous_run'],
        ),
        'node_c': build_node_c_handoff(
            headline_metrics,
            bottleneck_classes,
            hotspots,
            stall_breakdown,
            provisional_analysis['delta_vs_previous_run'],
        ),
    }
    return provisional_analysis


def render_analysis_md(analysis: Dict[str, Any]) -> str:
    launch = analysis.get('launch') or {}
    lines = ['# NCU analysis', '']
    lines.append(f"- schema version: `{analysis.get('schema_version')}`")
    lines.append(f"- status: `{analysis.get('status', 'unknown')}`")
    lines.append(f"- source run id: `{analysis.get('source_run_id', 'N/A')}`")
    lines.append(f"- source run dir: `{analysis.get('source_run_dir', 'N/A')}`")
    lines.append('')
    lines.append('## Launch')
    lines.append('')
    lines.append(f"- kernel name: `{launch.get('kernel_name', 'N/A')}`")
    lines.append(f"- block size: `{launch.get('block_size', 'N/A')}`")
    lines.append(f"- grid size: `{launch.get('grid_size', 'N/A')}`")
    lines.append(f"- registers / thread: `{launch.get('registers_per_thread', 'N/A')}`")
    lines.append(f"- shared mem / block allocated: `{launch.get('shared_mem_per_block_allocated', 'N/A')}`")
    lines.append('')
    lines.append('## Headline metrics')
    lines.append('')
    headline_metrics = analysis.get('headline_metrics') or {}
    if headline_metrics:
        for key, value in headline_metrics.items():
            lines.append(f"- `{key}`: `{value}`")
    else:
        lines.append('No headline metrics are available.')
    lines.append('')
    lines.append('## Primary bottlenecks')
    lines.append('')
    bottlenecks = analysis.get('bottleneck_classes') or []
    if bottlenecks:
        for item in bottlenecks[:6]:
            lines.append(
                f"- `{item.get('class_id')}` | severity `{item.get('severity_score')}` | {item.get('summary')}"
            )
    else:
        lines.append('No bottleneck classes were derived.')
    lines.append('')
    lines.append('## Stall breakdown')
    lines.append('')
    stalls = analysis.get('stall_breakdown') or []
    if stalls:
        for item in stalls:
            lines.append(f"- `{item.get('stall_group')}`: `{item.get('metric_value')}` | {item.get('explanation')}")
    else:
        lines.append('No structured stall breakdown is available.')
    lines.append('')
    lines.append('## Top hotspots')
    lines.append('')
    hotspots = analysis.get('source_hotspots') or []
    if hotspots:
        for hotspot in hotspots[:TOP_HOTSPOT_LIMIT]:
            lines.append(
                f"- `{hotspot.get('scope_type')}` `{hotspot.get('scope_name')}` @ `{hotspot.get('location', 'N/A')}` | "
                f"`{hotspot.get('metric_name')}` = `{hotspot.get('metric_value')}` | {hotspot.get('explanation')}"
            )
    else:
        lines.append('No source or section hotspots are available.')
    lines.append('')
    lines.append('## Delta vs previous run')
    lines.append('')
    delta_summary = analysis.get('delta_vs_previous_run') or {}
    lines.append(f"- baseline run id: `{delta_summary.get('baseline_run_id', 'N/A')}`")
    for item in (delta_summary.get('stall_breakdown') or [])[:4]:
        lines.append(
            f"- stall `{item.get('stall_group')}`: current `{item.get('current')}` vs previous `{item.get('previous')}` | "
            f"delta `{item.get('delta')}` | trend `{item.get('trend')}`"
        )
    hotspot_buckets = delta_summary.get('source_hotspots') or {}
    for bucket_name in ('regressed', 'new', 'improved', 'disappeared'):
        bucket = hotspot_buckets.get(bucket_name) or []
        if not bucket:
            continue
        lines.append(f"- hotspot delta `{bucket_name}`:")
        for item in bucket[:2]:
            lines.append(
                f"  - `{item.get('scope_name') or item.get('location')}` | `{item.get('metric_name')}` | trend `{item.get('trend')}`"
            )
    lines.append('')
    lines.append('## Handoff to node_b')
    lines.append('')
    node_b = (analysis.get('handoff') or {}).get('node_b') or {}
    for finding in node_b.get('top_findings', []):
        lines.append(f"- `{finding.get('finding_type')}`: {finding.get('summary')}")
    lines.append('')
    lines.append('## Handoff to node_c')
    lines.append('')
    node_c = (analysis.get('handoff') or {}).get('node_c') or {}
    for hotspot in node_c.get('target_hotspots', [])[:4]:
        lines.append(f"- target hotspot `{hotspot.get('scope_name')}` @ `{hotspot.get('location', 'N/A')}`")
    for guardrail in node_c.get('guardrail_metrics', [])[:4]:
        lines.append(
            f"- guardrail `{guardrail.get('metric_name')}`: `{guardrail.get('guardrail')}` from `{guardrail.get('current_value')}`"
        )
    lines.append('')
    lines.append('## Artifacts')
    lines.append('')
    artifacts = analysis.get('artifacts') or {}
    for key, payload in artifacts.items():
        lines.append(
            f"- `{key}`: status `{payload.get('status')}` | path `{payload.get('path', 'N/A')}`"
            + (f" | reason `{payload.get('unavailable_reason')}`" if payload.get('unavailable_reason') else '')
        )
    return '\n'.join(lines) + '\n'


def build_rich_summary_from_analysis(analysis: Dict[str, Any]) -> Dict[str, Any]:
    launch = analysis.get('launch') or {}
    artifacts = analysis.get('artifacts') or {}
    import_raw = artifacts.get('import_raw_page') or {}
    ncu_rep = artifacts.get('ncu_rep') or {}
    headline_csv = artifacts.get('headline_csv') or {}
    details_page = artifacts.get('details_page') or {}
    source_page = artifacts.get('source_page') or {}
    delta_summary = analysis.get('delta_vs_previous_run') or {}
    node_b = (analysis.get('handoff') or {}).get('node_b') or {}
    node_c = (analysis.get('handoff') or {}).get('node_c') or {}
    summary = {
        'schema_version': SCHEMA_VERSION,
        'status': analysis.get('status', 'missing'),
        'source_run_id': analysis.get('source_run_id'),
        'source_run_dir': analysis.get('source_run_dir'),
        'analysis_path': None,
        'kernel_name': launch.get('kernel_name'),
        'block_size': launch.get('block_size'),
        'grid_size': launch.get('grid_size'),
        'registers_per_thread': launch.get('registers_per_thread'),
        'shared_mem_per_block_allocated': launch.get('shared_mem_per_block_allocated'),
        'launch': launch,
        'headline_metrics': analysis.get('headline_metrics') or {},
        'stall_breakdown': list((analysis.get('stall_breakdown') or [])[:6]),
        'bottleneck_classes': [compact_bottleneck_class(item) for item in (analysis.get('bottleneck_classes') or [])[:6]],
        'top_findings': list((node_b.get('top_findings') or [])[:TOP_FINDING_LIMIT]),
        'top_source_hotspots': list((analysis.get('source_hotspots') or [])[:TOP_HOTSPOT_LIMIT]),
        'delta_vs_previous_run': compress_delta_for_summary(delta_summary),
        'handoff': {
            'node_b': {
                'top_findings': list((node_b.get('top_findings') or [])[:TOP_FINDING_LIMIT]),
                'code_regions_to_investigate': list((node_b.get('code_regions_to_investigate') or [])[:TOP_HOTSPOT_LIMIT]),
            },
            'node_c': {
                'target_hotspots': list((node_c.get('target_hotspots') or [])[:TOP_HOTSPOT_LIMIT]),
                'guardrail_metrics': list((node_c.get('guardrail_metrics') or [])[:6]),
                'expected_recheck_points': list((node_c.get('expected_recheck_points') or [])[:TOP_HOTSPOT_LIMIT]),
            },
        },
        'raw_csv_path': headline_csv.get('path'),
        'raw_rep_path': ncu_rep.get('path'),
        'raw_details_csv_path': import_raw.get('legacy_alias_path') or import_raw.get('path'),
        'import_raw_csv_path': import_raw.get('path'),
        'details_page_csv_path': details_page.get('path'),
        'source_csv_path': source_page.get('path'),
        'artifacts': artifacts,
    }
    return summary


def write_analysis_outputs(
    *,
    run_dir: Path,
    analysis: Dict[str, Any],
) -> Tuple[Path, Path]:
    analysis_json_path = run_dir / 'ncu_analysis.json'
    analysis_md_path = run_dir / 'ncu_analysis.md'
    write_json(analysis_json_path, analysis)
    write_text(analysis_md_path, render_analysis_md(analysis))
    return analysis_json_path, analysis_md_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Normalize and diagnose Nsight Compute artifacts into a stable schema.')
    parser.add_argument('--run-dir', type=Path, required=True)
    parser.add_argument('--source-run-id', required=True)
    parser.add_argument('--headline-csv', type=Path, default=None)
    parser.add_argument('--import-raw-csv', type=Path, default=None)
    parser.add_argument('--details-page-csv', type=Path, default=None)
    parser.add_argument('--source-csv', type=Path, default=None)
    parser.add_argument('--rep-path', type=Path, default=None)
    parser.add_argument('--legacy-import-raw-alias', type=Path, default=None)
    parser.add_argument('--previous-analysis', type=Path, default=None)
    parser.add_argument('--headline-metric', action='append', default=[])
    parser.add_argument('--source-unavailable-reason', default=None)
    parser.add_argument('--details-unavailable-reason', default=None)
    parser.add_argument('--import-raw-unavailable-reason', default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    analysis = analyze_run(
        run_dir=args.run_dir,
        source_run_id=args.source_run_id,
        headline_csv_path=args.headline_csv,
        import_raw_path=args.import_raw_csv,
        details_page_path=args.details_page_csv,
        source_csv_path=args.source_csv,
        rep_path=args.rep_path,
        wanted_headline_metrics=args.headline_metric,
        previous_analysis_path=args.previous_analysis,
        source_unavailable_reason=args.source_unavailable_reason,
        details_unavailable_reason=args.details_unavailable_reason,
        import_raw_unavailable_reason=args.import_raw_unavailable_reason,
        legacy_import_raw_alias=args.legacy_import_raw_alias,
    )
    write_analysis_outputs(run_dir=args.run_dir, analysis=analysis)


if __name__ == '__main__':
    main()
