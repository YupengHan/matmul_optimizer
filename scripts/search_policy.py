#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from typing import Any, Dict


def normalize_risk_text_to_level(risk_text: str | None) -> int:
    """Map free-form risk text to a coarse integer level.

    Levels:
    - 0: low
    - 1: moderate / medium / unknown
    - 2: high
    - 3: structural / invasive
    """

    if not risk_text:
        return 1
    text = risk_text.strip().lower()
    if 'structural' in text or 'invasive' in text:
        return 3
    if 'high' in text:
        return 2
    if 'moderate' in text or 'medium' in text:
        return 1
    if 'low' in text:
        return 0
    return 1


def fallback_search_score_v1(rank: int, recommended: bool, risk_text: str | None) -> float:
    rank_score = 4 - int(rank)
    recommended_bonus = 0.25 if recommended else 0.0
    risk_level = normalize_risk_text_to_level(risk_text)
    risk_penalty = {
        0: 0.0,
        1: 0.4,
        2: 0.9,
        3: 1.2,
    }[risk_level]
    return float(rank_score + recommended_bonus - risk_penalty)


def make_action_fingerprint(direction_dict: Dict[str, Any]) -> str:
    payload = {
        'name': (direction_dict.get('name') or '').strip(),
        'hypothesis': (direction_dict.get('hypothesis') or '').strip(),
        'expected_bottleneck': (direction_dict.get('expected_bottleneck') or '').strip(),
        'code_locations': sorted(str(item).strip() for item in direction_dict.get('code_locations', []) if str(item).strip()),
        'metrics_to_recheck': sorted(str(item).strip() for item in direction_dict.get('metrics_to_recheck', []) if str(item).strip()),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    return hashlib.sha1(canonical.encode('utf-8')).hexdigest()[:16]


def classify_transition(
    prev_runtime_ms: float | None,
    curr_runtime_ms: float | None,
    correctness_passed: bool | None,
    *,
    build_status: str | None = 'PASS',
    predicted_gain_ms: float | None = None,
    enable_diag_pos_runtime_neg: bool = False,
) -> Dict[str, Any]:
    flat_threshold_ms = 0.05
    normalized_build_status = (build_status or 'PASS').strip().upper()
    predicted_positive = predicted_gain_ms is not None and float(predicted_gain_ms) > 0.0

    if normalized_build_status != 'PASS':
        return {
            'transition_label': 'BUILD_FAIL',
            'transition_class': 'build_failed',
            'correctness_passed': correctness_passed,
            'runtime_delta_ms': None,
            'runtime_delta_label': None,
            'flat_threshold_ms': flat_threshold_ms,
            'predicted_gain_ms': predicted_gain_ms,
            'diag_pos_runtime_neg_eligible': False,
        }

    if correctness_passed is False:
        return {
            'transition_label': 'CORRECTNESS_FAIL',
            'transition_class': 'correctness_failed',
            'correctness_passed': False,
            'runtime_delta_ms': None,
            'runtime_delta_label': None,
            'flat_threshold_ms': flat_threshold_ms,
            'predicted_gain_ms': predicted_gain_ms,
            'diag_pos_runtime_neg_eligible': False,
        }

    if prev_runtime_ms is None or curr_runtime_ms is None:
        return {
            'transition_label': 'UNMEASURED',
            'transition_class': 'unmeasured',
            'correctness_passed': correctness_passed,
            'runtime_delta_ms': None,
            'runtime_delta_label': None,
            'flat_threshold_ms': flat_threshold_ms,
            'predicted_gain_ms': predicted_gain_ms,
            'diag_pos_runtime_neg_eligible': False,
        }

    runtime_delta_ms = float(curr_runtime_ms) - float(prev_runtime_ms)
    if abs(runtime_delta_ms) < flat_threshold_ms:
        transition_label = 'PASS_FLAT'
        transition_class = 'flat'
        runtime_delta_label = 'flat'
    elif runtime_delta_ms < 0:
        transition_label = 'PASS_WIN'
        transition_class = 'improved'
        runtime_delta_label = 'improved'
    else:
        if predicted_positive and enable_diag_pos_runtime_neg:
            transition_label = 'DIAG_POS_RUNTIME_NEG'
        else:
            transition_label = 'PASS_LOSS'
        transition_class = 'regressed'
        runtime_delta_label = 'regressed'

    return {
        'transition_label': transition_label,
        'transition_class': transition_class,
        'correctness_passed': correctness_passed,
        'runtime_delta_ms': runtime_delta_ms,
        'runtime_delta_label': runtime_delta_label,
        'flat_threshold_ms': flat_threshold_ms,
        'predicted_gain_ms': predicted_gain_ms,
        'diag_pos_runtime_neg_eligible': bool(predicted_positive and runtime_delta_ms > 0),
    }
