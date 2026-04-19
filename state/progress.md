# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `awaiting_direction_selection_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `15d63b2993c6eecc3a912dc4a648de6294e82efc`
- plateau counter: `3`
- round loop: `round 1/5`
- rounds remaining: `5`
- notes: `Node B completed. Approve a direction or explicitly use the recommended direction before node_c.`

## Latest measured custom run

- run id: `20260419_122438_bf16_gemm_v1_15d63b2`
- run dir: `runs/20260419_122438_bf16_gemm_v1_15d63b2`
- correctness: `PASS`
- median runtime: `35.725824 ms`
- TFLOP/s: `20.349969 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_122507`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Diagnosed accepted base run 20260419_122438_bf16_gemm_v1_15d63b2 at 35.725824 ms. The human-priority direction is ranked first and recommended: keep the single-skew 64x384 macro tile and test a warp-specialized producer/consumer split in the peeled hot kernel. The current measured bottlenecks are coherent with that choice: tensor active remains only 34.86 while barrier stall is 15.23, mio_throttle is 35.53, and hot-kernel LSU pressure is already high. The other two directions stay bounded and avoid reopening macro-tile changes.`
- dir_01: Warp-specialize the peeled 64x384 hot loop into producer and consumer warps | bottleneck: All-warps staging and CTA-wide stage handoff in the peeled 64x384 hot kernel, which can suppress tensor issue even when occupancy is still healthy at the current 2-block register limit.
- dir_02: Pair Tile384 epilogue export across the existing two C-scratch stages | bottleneck: Hot-kernel shared export and LSU traffic after MMA completion, which can still contribute to the current mio_throttle even when the main loop is well scheduled.
- dir_03: Add a fixed-K peeled 64x96 tail kernel | bottleneck: Residual generic-loop, barrier, and scoreboard overhead in the 64x96 tail kernel; upside is capped because the tail is only a small share of total wall time.

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `8.737343 ms`, `1.337116x` slower than CUTLASS
