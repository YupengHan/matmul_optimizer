# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 31/50` with `20` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_002707`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 31: L2 Cache is promoted again, but specifically because the branch conditions changed after the original grouped-order sweep. The current best branch now combines grouped ordering, `launch_bounds(128, 2)`, and unroll-2, so re-checking the nearby grouped setting is more justified than repeating unrelated hot-band ideas. Register Reuse and compiler guidance remain accepted in the background because they define the current base. K32, peeled scheduling, aggressive launch-bounds, and 256x128 remain rejected.`
- dir_01: Restore the current best branch and re-test grouped_rows=4 under the newer launch-bounds plus unroll-2 codegen | bottleneck: Cross-CTA locality under the newer compiler-guided hot-band branch, not under the earlier baseline used in the first grouped-order sweep.
- dir_02: Freeze the current best hot-band branch and start trimming the smaller non-hot-band remainder only if the grouped re-check is neutral | bottleneck: Secondary-region overhead outside the main hot band.
- dir_03: Hold the current best branch fixed and revisit tiny barrier-side cleanup only after the grouped re-check is settled | bottleneck: Residual barrier overhead in the current best hot-band kernel.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
