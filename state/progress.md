# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `d90a8731b2f67bd39feb4960efeb9b70068ce838`
- plateau counter: `1`
- round loop: `round 2/5`
- rounds remaining: `4`
- notes: `Node C build succeeded for round 2/5. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_093633_bf16_gemm_v1_d90a873`
- run dir: `runs/20260419_093633_bf16_gemm_v1_d90a873`
- correctness: `PASS`
- median runtime: `42.341888 ms`
- TFLOP/s: `17.170217 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_093742`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- diagnosis notes: `Round 2/5 diagnosis prepared from regressed run 20260419_093633_bf16_gemm_v1_d90a873. Round-1 two-level B staging is treated as negative evidence; recommendation pivots to the human phased-64x384 idea on the restored accepted base surface.`
- dir_01: Phased 64x384 micro-panels to shrink the live set | bottleneck: Register-limited occupancy and weak latency hiding from the 12-fragment live set in the hot 64x384 loop.
- dir_02: Simplify the 64x384 K-loop pipeline instead of repacking B | bottleneck: CTA-wide synchronization and copy-pipeline issue pressure in the hot loop.
- dir_03: Trim the 64x384 epilogue export path on the restored single-skew base | bottleneck: LSU/shared writeback pressure and epilogue-side shared-memory traffic after the main MMA loop.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `human_idea`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `11.367918 ms`, `1.438613x` slower than CUTLASS
