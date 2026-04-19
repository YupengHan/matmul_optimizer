# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 9/20` with `12` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_233315`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9 intentionally includes substantial human-in-loop guidance and a more exploratory, out-of-box diagnosis mindset. Using docs/heuristics.md explicitly, the current profile reads as a mixed global-memory plus synchronization plus instruction-mix imbalance, not a small tail or prologue-cleanup problem; at 56.87 ms, the kernel is still far from the ~20 ms long-horizon ceiling, so the ranking favors structural changes over another incremental K-loop prologue/steady-state/drain tweak. Round 9 node_c should restore to the round-7 measured commit before applying the selected direction.`
- dir_01: Retile to a 64x96 CTA so each staged B tile feeds more MMA before the next sync | bottleneck: Global-memory and LSU-heavy instruction mix starving Tensor Cores; the current shared-limited 7-block residency caps the kernel near 28 active warps/SM and still leaves too little math per staged K slice.
- dir_02: Remove the shared-memory epilogue scratch and recover occupancy plus LSU budget for the steady state | bottleneck: Shared-memory footprint and epilogue LSU traffic are reinforcing the same MIO/LSU congestion seen in the profile and are blocking higher CTA residency even though registers are not the limiting resource.
- dir_03: Replace the lockstep double buffer with a more overlapped producer-consumer cp.async pipeline | bottleneck: Synchronization and MIO throttle inside the steady-state K loop; the current double-buffered design still executes as a block-wide phase machine rather than a truly overlapped pipeline.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
