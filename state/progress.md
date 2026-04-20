# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `a4dc9684180bd8d536161425ebd8373caf288a6e`
- plateau counter: `29`
- round loop: `round 4/17`
- rounds remaining: `14`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 4/17.`

## Latest measured custom run

- run id: `20260420_155035_bf16_gemm_v1_a4dc968`
- run dir: `runs/20260420_155035_bf16_gemm_v1_a4dc968`
- correctness: `PASS`
- median runtime: `25.545729 ms`
- TFLOP/s: `28.459530 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_155107`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4/17 diagnosis for run 20260420_155035_bf16_gemm_v1_a4dc968. Human-review mapping: keep broad default-promotion, staged K32, paired export-lifetime, x-major traversal, and deeper export flattening closed; continue to accept only narrow PTX-adjacent moves on top of the accepted base 20260420_154827_bf16_gemm_v1_7adfc4e at 25.50532818 ms. The round-3 result shows the export family has likely plateaued: DRAM stayed healthy at 11.52, but the extra TileRow flattening regressed runtime by 0.0404005 ms and pushed long-scoreboard back to 7.75. That makes PTX prefetch handoff the best next move, with B-shared skew as the main alternate family and only a minimal export-side cleanup retained as a low-risk control.`
- dir_01: Retune PTX Prefetch Handoff On Top Of The Accepted Export Base | bottleneck: Copy-pipeline handoff timing in the PTX hot-band steady-state loop.
- dir_02: Tune PTX Hot-Band B-Shared Skew On The New Base | bottleneck: Shared-memory fragment address generation and B-tile layout friction in the PTX hot-band path.
- dir_03: Apply Only A Minimal PTX Export Address Cleanup | bottleneck: Residual address-generation overhead in the PTX export helper on top of the accepted one-stage scratch design.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
