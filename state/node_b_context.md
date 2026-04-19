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
- `runs/20260418_111959_bf16_gemm_v1_host_v0/summary.json`
- `runs/20260418_111959_bf16_gemm_v1_host_v0/ncu_metrics.csv`

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
- latest run id: `20260418_111959_bf16_gemm_v1_host_v0`
- median runtime: `802.842560 ms`
- TFLOP/s: `0.905557 TFLOP/s`
- measured commit: `9e20de18aa67dc6b5eb289d5e8e4c203dae37fa6`
- existing diagnosis status: `awaiting_codex`
