# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 2/5` with `4` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_123318`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- diagnosis notes: `Diagnosed regressed round-1 run 20260419_123228_bf16_gemm_v1_1dd4420 while ranking follow-ups against the restored accepted base 15d63b2. The warp-specialized producer/consumer split is strong negative evidence: it pushed the hot kernel to 219 registers per thread, dropped occupancy_limit_registers to 1, cut active warps to 16.60, and regressed to 42.259968 ms. The recommended follow-up therefore keeps the accepted 64x384 macro shape and targets lower-risk fixed-shape control overhead by splitting the hot path into explicit prologue, steady-state, and epilogue phases.`
- dir_01: Split the fixed 64x384 hot path into explicit prologue, steady-state, and epilogue phases | bottleneck: Fixed-shape hot-loop control and stage-transition overhead in the restored 64x384 peeled kernel, where tensor activity is still only 34.86 despite stable 2-block occupancy.
- dir_02: Straight-line the Tile384 cp.async producer schedule without warp specialization | bottleneck: Producer-side cp.async issue overhead and LSU address work in the hot kernel, without changing warp roles or macro-tile shape.
- dir_03: Add a fixed-K peeled 64x96 tail kernel | bottleneck: Residual generic-loop, barrier, and scoreboard overhead in the 64x96 tail kernel; total upside is capped by the tail's small share of wall time.

## Active direction

- selected direction: `dir_01`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
