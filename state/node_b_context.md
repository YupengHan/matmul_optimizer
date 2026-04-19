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
- `runs/20260418_212022_bf16_gemm_v1_deeb976/summary.json`
- `runs/20260418_212022_bf16_gemm_v1_deeb976/ncu_metrics.csv`

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

- round loop: `round 3/5`
- rounds remaining after this one: `2`
- latest run id: `20260418_212022_bf16_gemm_v1_deeb976`
- median runtime: `101.616016 ms`
- TFLOP/s: `7.154575 TFLOP/s`
- measured commit: `deeb9765cb3ed49aa93e1d9cefc6b3beacd950f5`
- existing diagnosis status: `pending_generation`
