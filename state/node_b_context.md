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
- `runs/20260419_011243_bf16_gemm_v1_33e1461/summary.json`
- `runs/20260419_011243_bf16_gemm_v1_33e1461/ncu_metrics.csv`
- `runs/20260419_011243_bf16_gemm_v1_33e1461/ncu_details.csv`
- `runs/20260419_011243_bf16_gemm_v1_33e1461/ncu_profile.ncu-rep`

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

- round loop: `round 18/20`
- rounds remaining after this one: `2`
- latest run id: `20260419_011243_bf16_gemm_v1_33e1461`
- median runtime: `41.534977 ms`
- TFLOP/s: `17.503788 TFLOP/s`
- measured commit: `33e1461e09c0f90b0896452a94c16277f2a251db`
- existing diagnosis status: `pending_generation`
