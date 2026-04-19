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
- `runs/20260418_221951_bf16_gemm_v1_eecbb72/summary.json`
- `runs/20260418_221951_bf16_gemm_v1_eecbb72/ncu_metrics.csv`

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

- round loop: `round 2/20`
- rounds remaining after this one: `18`
- latest run id: `20260418_221951_bf16_gemm_v1_eecbb72`
- median runtime: `82.266624 ms`
- TFLOP/s: `8.837356 TFLOP/s`
- measured commit: `eecbb72cf2ce923b80d7eab679b5355a3873fc88`
- existing diagnosis status: `completed`
