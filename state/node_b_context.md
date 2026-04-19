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
- `runs/20260418_224421_bf16_gemm_v1_f5de2e9/summary.json`
- `runs/20260418_224421_bf16_gemm_v1_f5de2e9/ncu_metrics.csv`
- `runs/20260418_224421_bf16_gemm_v1_f5de2e9/ncu_details.csv`
- `runs/20260418_224421_bf16_gemm_v1_f5de2e9/ncu_profile.ncu-rep`

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

- round loop: `round 4/20`
- rounds remaining after this one: `16`
- latest run id: `20260418_224421_bf16_gemm_v1_f5de2e9`
- median runtime: `65.617920 ms`
- TFLOP/s: `11.079587 TFLOP/s`
- measured commit: `f5de2e9ce546b72f0e2b1ecde0fbe5a766a31e42`
- existing diagnosis status: `completed`
