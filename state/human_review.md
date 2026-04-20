# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 25/50` with `26` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_001618`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 25: Register Reuse / compiler guidance is promoted again because the mild launch-bounds clue produced the largest single-round gain in this recent stretch, while the grouped-order L2 tuning has already identified a strong base at grouped_rows=8. L2 Cache remains accepted and now effectively baked into the base branch. Stage, Async Copy, Data Reuse, Pg2s, and Ps2r remain accepted background infrastructure. Tiling 256x128 stays rejected, and aggressive launch-bounds remains rejected, but the measured 2-CTA regime makes `launch_bounds(128, 2)` the next sensible refinement.`
- dir_01: Keep grouped_rows=8 and refine the compiler clue to a two-argument launch-bounds target of 2 resident CTAs | bottleneck: Compiler allocation / instruction scheduling quality on the accepted grouped-order hot-band kernel, now that the preferred 2-CTA regime is visible in measured data.
- dir_02: Keep the new best grouped-order base unchanged and return to conservative barrier-side cleanup | bottleneck: Residual barrier overhead under the new best grouped-order + launch-bounds base.
- dir_03: Freeze the current best branch and revisit a neighboring grouped-order value only if compiler refinement stalls | bottleneck: Fine-grained L2-order tuning around the current best base.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
