# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `9d84c09b3ca47275ec766af61a4a51c0a4ebdcee`
- plateau counter: `3`
- round loop: `round 8/30`
- rounds remaining: `23`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 8/30.`

## Latest measured custom run

- run id: `20260419_221757_bf16_gemm_v1_9d84c09`
- run dir: `runs/20260419_221757_bf16_gemm_v1_9d84c09`
- correctness: `PASS`
- median runtime: `30.769152 ms`
- TFLOP/s: `23.628192 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_221835`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 8/30 starts from a clearly negative warp-local consumer-order experiment. Reversing the mirrored 64x64 B sweep to a `Right Left Right Left` order preserved correctness but regressed runtime by about 0.46 ms, slowed the hot-band kernel to about 41.76 us, and worsened tensor active, barrier stall, short scoreboard, and `mio_throttle`. The next move should therefore restore the proven pre-sweep consumer path and spend one round on a different human-idea family. Recommended direction dir_01 does exactly that while also trying the fixed-shape stage-peeling idea on the hot-band K loop. Dir_02 keeps the cp.async ownership experiment ready on the same restored surface, and dir_03 is the pure restore fallback if the peeling change grows too large.`
- dir_01: Human idea stage: restore the pre-sweep best surface and peel the hot-band K loop into steady-state | bottleneck: Fixed-shape control-flow and stage-transition overhead inside the hot-band K loop.
- dir_02: Human idea coalescing + async copy: restore the pre-sweep best surface and retune cp.async ownership | bottleneck: Global-to-shared staging issue regularity and LSU ownership balance.
- dir_03: Restore the pre-sweep best surface without adding a new experiment | bottleneck: Not a direct bottleneck attack; this is a branch repair after a negative warp-local consumer experiment.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.514943 ms`, `1.135618x` slower than CUTLASS
