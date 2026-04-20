# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 28/50` with `23` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_002144`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 28: Register Reuse / compiler scheduling remains the primary family because grouped ordering and `launch_bounds(128, 2)` are already fixed into the base, and the first unroll increase produced another large measured gain. L2 Cache stays accepted and fixed at grouped_rows=8. Stage remains accepted as background structure but is no longer the first lever to perturb. Tiling 256x128, aggressive launch-bounds, and the peeled schedule remain rejected.`
- dir_01: Keep the current best branch and raise the hot-band K16 loop to the next small unroll factor | bottleneck: Residual loop-control and scheduling overhead in the current best hot-band K16 kernel.
- dir_02: Freeze the current best branch and revisit one more mild compiler clue only if higher unrolling stalls | bottleneck: Compiler codegen refinement on the grouped_rows=8 plus `launch_bounds(128, 2)` base.
- dir_03: Hold the current best branch fixed and return to tiny barrier-side cleanup only if compiler tuning saturates | bottleneck: Residual barrier overhead in the current best hot-band kernel.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
