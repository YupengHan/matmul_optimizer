# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `0a38a28b4a1fe020ff734c847e555a8d67bbfa48`
- plateau counter: `10`
- round loop: `round 11/50`
- rounds remaining: `40`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 11/50.`

## Latest measured custom run

- run id: `20260419_231125_bf16_gemm_v1_0a38a28`
- run dir: `runs/20260419_231125_bf16_gemm_v1_0a38a28`
- correctness: `PASS`
- median runtime: `30.355456 ms`
- TFLOP/s: `23.950206 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_231228`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 11/50 moves from the flat L2 swizzle to the next human-idea family: Pg2s orchestration. The recommended next move is dir_01, a conservative half-CTA staging subset that keeps tile shape, control flow, and the consumer microkernel intact while reducing the number of threads issuing async copies in the hot-band kernel.`
- dir_01: Keep the restored correct surface and let only half the CTA issue hot-band Pg2s async copies | bottleneck: CTA-level staging orchestration and LSU/shared issue pressure during Pg2s rather than warp-local MMA scheduling.
- dir_02: Keep the restored surface and try a light consumer-side B XOR swizzle instead of extra padding | bottleneck: Shared-memory bank behavior on the B operand path without adding CTA-level repacking.
- dir_03: Restore-only fallback to the accepted-correct surface | bottleneck: Not a bottleneck attack; this is the reset path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
