# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 3/50` with `48` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_223942`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3/50 starts from another small bank-padding regression. The hot-band path remains dominant, and the recent local layout/export tweaks have not produced a durable win. Recommended direction dir_01 therefore moves to a larger but still coherent structural change: restore the current best surface and replace the final 64 hot rows with a dedicated 64x128 residual PTX kernel so those rows stop paying the 384 peeled path. Dir_02 is the restore fallback if that kernel does not validate quickly, and dir_03 defers any more export work until the residual path is specialized.`
- dir_01: Restore the best surface and replace the last 64 hot rows with a dedicated 64x128 residual PTX kernel | bottleneck: Residual hot-row overhead from routing the last 64 rows through the generic 384 peeled kernel instead of a matching fixed-shape PTX path.
- dir_02: Restore-only fallback to the current best surface | bottleneck: Not a bottleneck attack; this is the restore path after a negative bank-padding experiment.
- dir_03: Later: revisit export trimming only after the residual path is specialized | bottleneck: Shared epilogue/export overhead after the residual path has been unified with the PTX hot-band family.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
