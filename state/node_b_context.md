# Node B context

Node B is the diagnosis node. Read the files below, then write exactly three directions to `state/latest_diagnosis.json`.

## Read order

- `state/latest_run.md`
- `state/latest_ncu_summary.md`
- `docs/heuristics.md`
- `state/progress.md`
- `state/current_focus.md`
- `state/human_review.md`
- `src/kernels/bf16_gemm_v1.cu`
- `runs/20260419_002954_bf16_gemm_v1_0ac7611/summary.json`
- `runs/20260419_002954_bf16_gemm_v1_0ac7611/ncu_metrics.csv`
- `runs/20260419_002954_bf16_gemm_v1_0ac7611/ncu_details.csv`
- `runs/20260419_002954_bf16_gemm_v1_0ac7611/ncu_profile.ncu-rep`

Use the raw detailed CSV when the headline summary is too shallow to explain pipeline, memory, or bank-conflict behavior.

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

- round loop: `round 14/20`
- rounds remaining after this one: `6`
- latest run id: `20260419_002954_bf16_gemm_v1_0ac7611`
- median runtime: `65.610237 ms`
- TFLOP/s: `11.080884 TFLOP/s`
- measured commit: `0ac7611b334ecc5aed0106a24dfae3c2125360d8`
- existing diagnosis status: `completed`
