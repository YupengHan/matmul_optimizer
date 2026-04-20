# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `0cbbcf7b2d28ba864853823c4120f8f0001843a1`
- plateau counter: `2`
- round loop: `round 24/50`
- rounds remaining: `27`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 24/50.`

## Latest measured custom run

- run id: `20260420_001413_bf16_gemm_v1_0cbbcf7`
- run dir: `runs/20260420_001413_bf16_gemm_v1_0cbbcf7`
- correctness: `PASS`
- median runtime: `29.179888 ms`
- TFLOP/s: `24.915086 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_001453`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 24: L2 Cache has now produced the best measured branch and `grouped_rows=8` appears to be the best tested setting, so the next step is to keep that gain and combine it with the mildest plausible compiler clue from the Register Reuse family. Stage, Async Copy, Data Reuse, Pg2s, and Ps2r remain accepted background infrastructure. Tiling 256x128 stays rejected. Aggressive launch-bounds remains rejected, but a single-argument launch-bounds hint is materially different and lower risk. Coalescing Access and Bank Conflict remain deferred.`
- dir_01: Restore grouped_rows=8 and try a single-argument launch-bounds clue on the accepted hot-band kernel | bottleneck: Compiler allocation / scheduling quality on top of the accepted grouped-order 128x128 K16 kernel.
- dir_02: Accept grouped_rows=8 as fixed and return to conservative K16 barrier cleanup | bottleneck: Residual barrier overhead in the accepted grouped-order K16 kernel.
- dir_03: Keep the grouped_rows=8 base and test one intermediate grouped-order value only if compiler and stage tweaks stall | bottleneck: Fine-grained cache-locality tuning around the accepted grouped-order base.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.031615 ms`, `1.116970x` slower than CUTLASS
