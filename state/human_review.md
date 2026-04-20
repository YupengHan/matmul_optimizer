# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 27/50` with `24` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_002004`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 27: Stage remains relevant, but after the failed peeled rewrite the right interpretation is now 'reduce control overhead gently' rather than 'rewrite the loop schedule.' Register Reuse / compiler guidance also remains active because the best branch still relies on grouped L2 ordering plus `launch_bounds(128, 2)`. L2 Cache stays accepted and fixed at grouped_rows=8. Tiling 256x128, aggressive launch-bounds, and the peeled schedule are now rejected on measured evidence. Coalescing Access and Bank Conflict remain deferred.`
- dir_01: Restore the current best branch and raise the hot-band K16 loop from unroll-1 to a small fixed unroll factor | bottleneck: Loop-control overhead in the accepted hot-band K16 kernel, approached through milder compiler unrolling rather than manual schedule peeling.
- dir_02: Restore the current best branch unchanged and revisit tiny barrier-side cleanup only if unrolling stalls | bottleneck: Residual barrier overhead under the grouped_rows=8 plus `launch_bounds(128, 2)` base.
- dir_03: Freeze the current best branch and revisit a neighboring compiler clue only after the unroll result is known | bottleneck: Compiler codegen refinement on the current best branch.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
