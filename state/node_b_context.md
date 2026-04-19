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
- `runs/20260418_230727_bf16_gemm_v1_2a86c71/summary.json`
- `runs/20260418_230727_bf16_gemm_v1_2a86c71/ncu_metrics.csv`
- `runs/20260418_230727_bf16_gemm_v1_2a86c71/ncu_details.csv`
- `runs/20260418_230727_bf16_gemm_v1_2a86c71/ncu_profile.ncu-rep`

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

- round loop: `round 7/20`
- rounds remaining after this one: `13`
- latest run id: `20260418_230727_bf16_gemm_v1_2a86c71`
- median runtime: `57.120176 ms`
- TFLOP/s: `12.727892 TFLOP/s`
- measured commit: `2a86c71387e520f89bd133d824161d17428f4242`
- existing diagnosis status: `pending_generation`
