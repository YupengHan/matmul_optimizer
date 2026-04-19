# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 8/20` with `13` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_232136`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Specialize the fixed-shape K loop so the 4-warp CTA spends less time in barrier and control overhead | bottleneck: Synchronization and hot-path control overhead in the double-buffered async-copy pipeline
- dir_02: Refine the same-footprint B shared layout so three `matrix_b` loads hit a friendlier per-warp pattern | bottleneck: Shared-memory B fragment load pressure and MIO saturation in the steady-state tensor loop
- dir_03: Attack the `c_shared` epilogue so the kernel sheds shared-memory footprint and MIO-heavy writeback work | bottleneck: Epilogue LSU/MIO pressure and shared-memory residency headroom lost to `c_shared`

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
