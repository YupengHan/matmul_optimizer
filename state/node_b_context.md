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
- `runs/20260418_201228_bf16_gemm_v1_af155a5/summary.json`
- `runs/20260418_201228_bf16_gemm_v1_af155a5/ncu_metrics.csv`

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
- latest run id: `20260418_201228_bf16_gemm_v1_af155a5`
- median runtime: `145.344559 ms`
- TFLOP/s: `5.002041 TFLOP/s`
- measured commit: `af155a5bdaa475a7edba5ed1957b25a46454536e`
- existing diagnosis status: `pending_generation`
