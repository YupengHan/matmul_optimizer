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
- `runs/20260418_210900_bf16_gemm_v1_aee3c09/summary.json`
- `runs/20260418_210900_bf16_gemm_v1_aee3c09/ncu_metrics.csv`

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

- round loop: `round 2/5`
- rounds remaining after this one: `3`
- latest run id: `20260418_210900_bf16_gemm_v1_aee3c09`
- median runtime: `101.374962 ms`
- TFLOP/s: `7.171588 TFLOP/s`
- measured commit: `aee3c09b51fbf78ad79f4ce5f68841449bab54a1`
- existing diagnosis status: `completed`
