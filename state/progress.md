# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `4fc47fd8dad9e9dd6b46dd22db57692a8f6d947e`
- plateau counter: `1`
- round loop: `round 23/50`
- rounds remaining: `28`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 23/50.`

## Latest measured custom run

- run id: `20260420_001248_bf16_gemm_v1_4fc47fd`
- run dir: `runs/20260420_001248_bf16_gemm_v1_4fc47fd`
- correctness: `PASS`
- median runtime: `29.319664 ms`
- TFLOP/s: `24.796308 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_001328`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 23: L2 Cache remains primary because grouped_rows=8 produced a real improvement and grouped_rows=16 provided useful negative evidence, which means this axis is still actively informative. Stage, Async Copy, Data Reuse, Pg2s, and Ps2r remain accepted fixed infrastructure under the current base. Register Reuse remains deferred after the launch-bounds failure. Tiling 256x128 stays rejected. Coalescing Access and Bank Conflict remain deferred because the current wins and losses are still tracking CTA-order choices more than those signals.`
- dir_01: Keep the grouped CTA-order remap and reduce the hot-band row-group size to check the other side of the L2 curve | bottleneck: Cross-CTA cache locality on the accepted grouped-order hot-band kernel.
- dir_02: Hold grouped_rows=8 as the accepted L2 base and return to conservative K16 barrier-side cleanup | bottleneck: Residual barrier overhead in the accepted grouped-order K16 kernel.
- dir_03: Freeze the accepted grouped-order kernel and revisit a strictly milder register hint later | bottleneck: Compiler allocation quality on top of the accepted grouped-order base.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.031615 ms`, `1.116970x` slower than CUTLASS
