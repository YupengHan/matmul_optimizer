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
- `runs/20260418_220017_bf16_gemm_v1_2e79574/summary.json`
- `runs/20260418_220017_bf16_gemm_v1_2e79574/ncu_metrics.csv`

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

- round loop: `round 1/20`
- rounds remaining after this one: `19`
- latest run id: `20260418_220017_bf16_gemm_v1_2e79574`
- median runtime: `91.601360 ms`
- TFLOP/s: `7.936775 TFLOP/s`
- measured commit: `6600aebb6478a2fafe0e75f1780e596a9706e1d1`
- existing diagnosis status: `completed`
