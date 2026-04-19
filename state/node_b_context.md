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
- `runs/20260418_195405_bf16_gemm_v1_a4966f5/summary.json`
- `runs/20260418_195405_bf16_gemm_v1_a4966f5/ncu_metrics.csv`

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

- round loop: `single-run`
- rounds remaining after this one: `0`
- latest run id: `20260418_195405_bf16_gemm_v1_a4966f5`
- median runtime: `298.095123 ms`
- TFLOP/s: `2.438884 TFLOP/s`
- measured commit: `a4966f51626c0ae4e2d99e4e49fe26264639b123`
- existing diagnosis status: `completed`
