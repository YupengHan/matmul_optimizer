# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 26/50` with `25` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_001749`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 26: Stage is promoted again, but now in the fixed-shape-steady-state sense rather than a deeper buffering sense. The current best branch already incorporates the accepted L2 Cache setting (`grouped_rows=8`) and the best measured compiler clue (`launch_bounds(128, 2)`), so the next rational move is to reduce control overhead in the fixed 452-tile K loop. Register Reuse remains accepted in the background because the best branch still depends on the compiler clue, but it is not the first thing to perturb this round. Tiling 256x128 and aggressive launch-bounds remain rejected. Coalescing Access and Bank Conflict remain deferred.`
- dir_01: Keep the current best branch and peel the fixed 452-tile K loop into steady-state plus epilogue | bottleneck: Mainloop control-flow and stage-transition overhead inside the accepted hot-band kernel.
- dir_02: Hold the current best branch fixed and return to tiny barrier-side cleanup only if peeling stalls | bottleneck: Residual barrier overhead under the current best grouped-order + launch-bounds(128,2) base.
- dir_03: Freeze the current best base and revisit one more moderate compiler clue only after the peeled schedule result is known | bottleneck: Compiler codegen refinement on top of the current best branch.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
