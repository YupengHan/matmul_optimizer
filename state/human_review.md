# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 3/20` with `18` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_222704`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Skew the B shared tile with a bank-conflict-avoidance swizzle | bottleneck: Residual bank conflicts and port contention on the shared-memory-to-WMMA B-fragment feed path, which still show up as `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct = 25.61` and `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct = 11.28` even after the tile-retune improvement.
- dir_02: Split the B tile into three independently padded 16x16 shared subtiles | bottleneck: The combined 16x48 row-major B layout may be making the three adjacent fragment loads interfere with each other at shared-memory bank granularity even though the per-warp compute reuse is otherwise correct.
- dir_03: Transpose B into a conflict-friendlier shared layout and switch the WMMA load orientation | bottleneck: The row-major B shared layout may be fundamentally mismatched to the warp-level matrix_b load pattern, keeping the tensor pipe underfed even after the earlier global-to-shared improvements.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
