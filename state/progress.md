# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `c2f2bec47c9cba44f35cf7d260893f0416a4d251`
- plateau counter: `0`
- round loop: `round 3/5`
- rounds remaining: `3`
- notes: `Node C build succeeded for round 3/5. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_132725_bf16_gemm_v1_c2f2bec`
- run dir: `runs/20260419_132725_bf16_gemm_v1_c2f2bec`
- correctness: `PASS`
- median runtime: `34.234447 ms`
- TFLOP/s: `21.236488 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_132801`
- recommended direction: `dir_01`
- approved direction: `dir_03`
- diagnosis notes: `All three directions stay strictly inside the 64x384 hot-band PTX microkernel branch and keep the 64x96 tail unchanged. Ranking explicitly uses the new fact that the PTX line has now delivered two consecutive real runtime improvements, including the round-2 win from replacing the array-style accumulator surface with 12 named tiles and compile-time expansion. Because occupancy_limit_registers is still 1 and active warps are still only 16.78, the next ranking prefers deeper PTX-local compute/load-order and live-state control over any switch back to WMMA or unrelated tile tuning.`
- dir_01: Ldmatrix plus panelized PTX hot-band compute control | bottleneck: Register-limited live state inside the current PTX hot-band compute path is holding occupancy at one block/SM; the branch now needs finer compute/load-order control to reduce residency pressure without abandoning the winning PTX line.
- dir_02: Register-first PTX export follow-through | bottleneck: The hot-band export path is still consuming shared/LSU issue budget and can now be a larger share of the remaining cost because mio throttle has already dropped sharply while runtime continues to improve.
- dir_03: Fixed-K PTX orchestration retime inside the peeled hot loop | bottleneck: Barrier and issue scheduling inside the fixed peeled loop are still interrupting tensor issue, even though the branch has already cut mio versus the WMMA base.

## Active implementation direction

- direction id: `dir_03`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `8.316559 ms`, `1.320881x` slower than CUTLASS
