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
- `runs/20260418_222639_bf16_gemm_v1_95056ed/summary.json`
- `runs/20260418_222639_bf16_gemm_v1_95056ed/ncu_metrics.csv`

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

- round loop: `round 3/20`
- rounds remaining after this one: `17`
- latest run id: `20260418_222639_bf16_gemm_v1_95056ed`
- median runtime: `66.354687 ms`
- TFLOP/s: `10.956565 TFLOP/s`
- measured commit: `95056ed21eab5afe9e0a7fc2faefa6e3b29e3903`
- existing diagnosis status: `pending_generation`
