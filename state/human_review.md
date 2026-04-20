# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 30/50` with `21` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_002530`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 30: Register Reuse / compiler scheduling remains primary because the winning branch is still moving on small compiler-guided loop-scheduling changes. L2 Cache remains accepted and fixed at grouped_rows=8. Stage remains accepted as background structure, but K32 is again rejected even under the newer base conditions. Tiling 256x128, aggressive launch-bounds, peeled scheduling, and K32 are all now rejected for the current search state.`
- dir_01: Restore the current best grouped K16 branch and test the intermediate unroll factor between 2 and 4 | bottleneck: Loop-control / scheduling overhead in the current best hot-band K16 kernel, with the unroll factor now being the only moving part.
- dir_02: Keep the current best hot-band branch fixed and begin trimming the smaller non-hot-band remainder only if unroll-3 stalls | bottleneck: Secondary-region overhead after hot-band optimization saturates.
- dir_03: Freeze the current best branch and revisit tiny barrier-side cleanup only after the unroll midpoint result is known | bottleneck: Residual barrier overhead in the grouped K16 winner.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
