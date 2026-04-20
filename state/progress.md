# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `a64854a656796209b16d18c89ea94794379b4ed6`
- plateau counter: `39`
- round loop: `round 14/17`
- rounds remaining: `4`
- notes: `Node C build succeeded for round 14/17. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_163357_bf16_gemm_v1_a64854a`
- run dir: `runs/20260420_163357_bf16_gemm_v1_a64854a`
- correctness: `PASS`
- median runtime: `33.964544 ms`
- TFLOP/s: `21.405246 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_163459`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 14/17 diagnosis for run 20260420_163357_bf16_gemm_v1_a64854a. Human-review mapping for this round: keep the 64x384 control closed after its catastrophic regression, and keep non-PTX 128x128 plus deeper export cleanup closed as well. The new evidence is decisive: the broad 64x384 path drove runtime to 33.9645443 ms, DRAM to 55.24, and barrier to 17.01, so the remaining search needs to stay inside the accepted default PTX launch rather than reopen broad alternate paths. No new explicit human idea family is queued in state/human_review.md, so the ranking narrows to the seam and residual PTX families: accept a one-block downward seam shift first, keep the 4-row grouping as the last PTX retry, and leave prefetch only as a tertiary scoreboard tradeoff if the cleaner options fail.`
- dir_01: Shift The Hot-Band / Peeled Seam Down By One PTX Block | bottleneck: Boundary and launch split cost between the PTX hot-band kernel and the peeled 384-row row-band path.
- dir_02: Keep The 4-Row PTX Grouping As The Last PTX Retry | bottleneck: Residual CTA grouping and orchestration overhead around the PTX hot-band grouped-row mapping.
- dir_03: Retry PTX Prefetch Only As A Last Scoreboard Tradeoff | bottleneck: Copy-pipeline handoff timing and future-tile refill cadence in the PTX hot-band steady-state loop.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
