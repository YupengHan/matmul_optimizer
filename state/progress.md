# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `81bde72e538f33c457ea3cac1335513761c90fd6`
- plateau counter: `40`
- round loop: `round 15/17`
- rounds remaining: `3`
- notes: `Node C build succeeded for round 15/17. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_163637_bf16_gemm_v1_81bde72`
- run dir: `runs/20260420_163637_bf16_gemm_v1_81bde72`
- correctness: `PASS`
- median runtime: `25.654704 ms`
- TFLOP/s: `28.338640 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_163723`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 15/17 diagnosis for run 20260420_163637_bf16_gemm_v1_81bde72. Human-review mapping for this round: keep the broad 64x384 control closed, keep non-PTX 128x128 closed, and keep deeper export cleanup closed. The fresh evidence is that the seam family is the cleanest remaining direction after the broad controls failed: shifting the pivot from 6400 to 6144 recovered the runtime to 25.65470409 ms with DRAM held to 11.25 and long-scoreboard at 5.91. No new explicit human idea family is queued in state/human_review.md, so the ranking now stays narrow for the last rounds: accept one more seam shift first, keep the 4-row grouping as the secondary PTX fallback, and leave prefetch only as a tertiary scoreboard tradeoff.`
- dir_01: Shift The Hot-Band / Peeled Seam Down One More 256-Row Chunk | bottleneck: Boundary and launch split cost between the PTX hot-band kernel and the peeled 384-row row-band path.
- dir_02: Keep The 4-Row PTX Grouping As The Last PTX Retry | bottleneck: Residual CTA grouping and orchestration overhead around the PTX hot-band grouped-row mapping.
- dir_03: Retry PTX Prefetch Only As A Final Scoreboard Tradeoff | bottleneck: Copy-pipeline handoff timing and future-tile refill cadence in the PTX hot-band steady-state loop.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
