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
- `runs/20260418_212627_bf16_gemm_v1_8138da5/summary.json`
- `runs/20260418_212627_bf16_gemm_v1_8138da5/ncu_metrics.csv`

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

- round loop: `round 4/5`
- rounds remaining after this one: `1`
- latest run id: `20260418_212627_bf16_gemm_v1_8138da5`
- median runtime: `97.885185 ms`
- TFLOP/s: `7.427267 TFLOP/s`
- measured commit: `8138da55448e546af314940addc89fd3cadc56ff`
- existing diagnosis status: `completed`
