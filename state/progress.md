# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `fe097e98f5e51da7e72c909a85c76f35a8c9508a`
- plateau counter: `2`
- round loop: `round 3/5`
- rounds remaining: `3`
- notes: `Node C build succeeded for round 3/5. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_094829_bf16_gemm_v1_fe097e9`
- run dir: `runs/20260419_094829_bf16_gemm_v1_fe097e9`
- correctness: `PASS`
- median runtime: `42.673632 ms`
- TFLOP/s: `17.036737 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_094909`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3/5 diagnosis prepared after the round-2 phased-64x384 experiment regressed to 42.673632 ms. Both recent human-guided families are treated as negative evidence on top of the restored accepted base 16a98f7 (37.285807 ms): round-1 two-level B staging regressed to 42.341888 ms and round-2 phased micro-panels regressed to 42.673632 ms. Ranking therefore pivots to other levers on the restored accepted base.`
- dir_01: Warp-specialize the 64x384 copy/compute pipeline on the restored base | bottleneck: CTA-wide synchronization and hot-loop feed orchestration in the 64x384 K-loop.
- dir_02: Peel a fixed-shape steady-state hot kernel for 6464x7776x7232 | bottleneck: Generic control-flow and stage-transition overhead diluting tensor issue in the fixed-shape hot loop.
- dir_03: Trim the c_shared epilogue/export path on the restored base | bottleneck: LSU/shared writeback pressure in the hot epilogue rather than another B-feed or live-set bottleneck family.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `11.367918 ms`, `1.438613x` slower than CUTLASS
