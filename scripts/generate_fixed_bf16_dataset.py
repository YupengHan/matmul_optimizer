#!/usr/bin/env python3
"""
Generate a deterministic fixed-shape BF16 GEMM dataset.

The generated dataset is intended to be:
- easy to load from both Python and C++,
- deterministic from seeds,
- and faithful to BF16 input quantization.

Output format per case:
    A.bf16.bin      raw uint16 BF16 bit-patterns, row-major
    B.bf16.bin      raw uint16 BF16 bit-patterns, row-major
    C_ref_fp32.bin  raw float32, row-major
    C_ref_bf16.bin  raw uint16 BF16 bit-patterns, row-major
    meta.json
    checksums.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np


def float32_to_bf16_bits(x: np.ndarray) -> np.ndarray:
    """Round float32 to BF16 and return raw uint16 bit patterns."""
    if x.dtype != np.float32:
        raise TypeError(f"expected float32, got {x.dtype}")
    x_u32 = x.view(np.uint32)
    lsb = (x_u32 >> 16) & np.uint32(1)
    rounding_bias = np.uint32(0x7FFF) + lsb
    bf16 = ((x_u32 + rounding_bias) >> 16).astype(np.uint16)
    return bf16


def bf16_bits_to_float32(bits: np.ndarray) -> np.ndarray:
    """Convert raw BF16 uint16 bit patterns back to float32."""
    if bits.dtype != np.uint16:
        raise TypeError(f"expected uint16 BF16 bits, got {bits.dtype}")
    as_u32 = bits.astype(np.uint32) << np.uint32(16)
    return as_u32.view(np.float32)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, payload: Dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + '\n', encoding='utf-8')


def generate_uniform_f32(rng: np.random.Generator, shape: tuple[int, int], low: float, high: float) -> np.ndarray:
    arr = rng.random(shape, dtype=np.float32)
    arr = arr * np.float32(high - low) + np.float32(low)
    return np.ascontiguousarray(arr, dtype=np.float32)


def ensure_empty_dir(path: Path, force: bool) -> None:
    if path.exists():
        if not force:
            raise FileExistsError(f"{path} already exists; use --force to overwrite")
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


@dataclass
class CaseConfig:
    case_id: str
    seed: int


def load_config(path: Path) -> Dict:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def write_case(dataset_dir: Path, config: Dict, case: CaseConfig, force: bool) -> Dict:
    gemm = config['gemm']
    dist = config['distribution']

    m = int(gemm['m'])
    n = int(gemm['n'])
    k = int(gemm['k'])
    low = float(dist['low'])
    high = float(dist['high'])

    case_dir = dataset_dir / 'cases' / case.case_id
    ensure_empty_dir(case_dir, force=force)

    rng = np.random.default_rng(case.seed)

    print(f"[generate] {case.case_id}: creating A({m}, {k}) and B({k}, {n})")
    a_f32 = generate_uniform_f32(rng, (m, k), low, high)
    b_f32 = generate_uniform_f32(rng, (k, n), low, high)

    print(f"[generate] {case.case_id}: quantizing inputs to BF16")
    a_bf16_bits = np.ascontiguousarray(float32_to_bf16_bits(a_f32))
    b_bf16_bits = np.ascontiguousarray(float32_to_bf16_bits(b_f32))

    del a_f32
    del b_f32

    print(f"[generate] {case.case_id}: reconstructing quantized float32 inputs")
    a_q_f32 = np.ascontiguousarray(bf16_bits_to_float32(a_bf16_bits))
    b_q_f32 = np.ascontiguousarray(bf16_bits_to_float32(b_bf16_bits))

    print(f"[generate] {case.case_id}: CPU GEMM reference in float32")
    c_ref_fp32 = np.ascontiguousarray(a_q_f32 @ b_q_f32, dtype=np.float32)

    del a_q_f32
    del b_q_f32

    print(f"[generate] {case.case_id}: quantizing reference output to BF16")
    c_ref_bf16_bits = np.ascontiguousarray(float32_to_bf16_bits(c_ref_fp32))

    files = {
        'A_bf16': case_dir / 'A.bf16.bin',
        'B_bf16': case_dir / 'B.bf16.bin',
        'C_ref_fp32': case_dir / 'C_ref_fp32.bin',
        'C_ref_bf16': case_dir / 'C_ref_bf16.bin',
    }

    print(f"[generate] {case.case_id}: writing raw binary payloads")
    a_bf16_bits.tofile(files['A_bf16'])
    b_bf16_bits.tofile(files['B_bf16'])
    c_ref_fp32.tofile(files['C_ref_fp32'])
    c_ref_bf16_bits.tofile(files['C_ref_bf16'])

    checksums = {name: sha256_file(path) for name, path in files.items()}
    write_json(case_dir / 'checksums.json', checksums)

    meta = {
        'case_id': case.case_id,
        'seed': case.seed,
        'm': m,
        'n': n,
        'k': k,
        'layout_a': gemm['layout_a'],
        'layout_b': gemm['layout_b'],
        'layout_c': gemm['layout_c'],
        'distribution': config['distribution'],
        'input_dtype': gemm['input_dtype'],
        'accumulator_dtype': gemm['accumulator_dtype'],
        'output_dtype': gemm['output_dtype'],
        'files': {
            'A_bf16': 'A.bf16.bin',
            'B_bf16': 'B.bf16.bin',
            'C_ref_fp32': 'C_ref_fp32.bin',
            'C_ref_bf16': 'C_ref_bf16.bin',
            'checksums': 'checksums.json',
        },
        'sizes_bytes': {
            'A_bf16': files['A_bf16'].stat().st_size,
            'B_bf16': files['B_bf16'].stat().st_size,
            'C_ref_fp32': files['C_ref_fp32'].stat().st_size,
            'C_ref_bf16': files['C_ref_bf16'].stat().st_size,
        },
    }
    write_json(case_dir / 'meta.json', meta)

    total_bytes = sum(meta['sizes_bytes'].values())
    print(f"[done] {case.case_id}: wrote {total_bytes / (1024 ** 2):.2f} MiB")

    return {
        'case_id': case.case_id,
        'seed': case.seed,
        'total_bytes': total_bytes,
        'checksums': checksums,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Generate the fixed BF16 GEMM dataset')
    parser.add_argument(
        '--config',
        type=Path,
        default=Path('configs/fixed_bf16_gemm_v1.json'),
        help='Path to dataset config JSON',
    )
    parser.add_argument(
        '--output-root',
        type=Path,
        default=Path('artifacts/datasets'),
        help='Root directory for generated datasets',
    )
    parser.add_argument(
        '--cases',
        nargs='*',
        default=None,
        help='Optional subset of case_ids to generate',
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing generated cases',
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    dataset_id = config['dataset_id']
    dataset_dir = args.output_root / dataset_id
    dataset_dir.mkdir(parents=True, exist_ok=True)

    selected = set(args.cases) if args.cases else None
    cases = [
        CaseConfig(case_id=item['case_id'], seed=int(item['seed']))
        for item in config['cases']
        if selected is None or item['case_id'] in selected
    ]
    if not cases:
        raise ValueError('No cases selected')

    manifest = {
        'dataset_id': dataset_id,
        'description': config['description'],
        'gemm': config['gemm'],
        'distribution': config['distribution'],
        'benchmark_policy': config['benchmark_policy'],
        'correctness_policy': config['correctness_policy'],
        'generated_cases': [case.case_id for case in cases],
    }
    write_json(dataset_dir / 'manifest.json', manifest)

    generated = []
    total_bytes = 0
    for case in cases:
        summary = write_case(dataset_dir, config, case, force=args.force)
        generated.append(summary)
        total_bytes += summary['total_bytes']

    root_summary = {
        'dataset_id': dataset_id,
        'generated_cases': generated,
        'total_bytes': total_bytes,
        'total_mib': total_bytes / (1024 ** 2),
    }
    write_json(dataset_dir / 'generation_summary.json', root_summary)

    print()
    print(f"[summary] dataset_id={dataset_id}")
    print(f"[summary] cases={len(generated)}")
    print(f"[summary] total_size={total_bytes / (1024 ** 2):.2f} MiB")
    print(f"[summary] manifest={dataset_dir / 'manifest.json'}")


if __name__ == '__main__':
    main()
