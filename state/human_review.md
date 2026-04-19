# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 5/20` with `16` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_225054`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Retile to a 4-warp CTA so each K-slice carries more MMA work and more resident warps | bottleneck: Occupancy ceiling and synchronization-limited tensor-core utilization in the steady-state mainloop
- dir_02: Replace the simple B-row skew with a stronger shared-memory swizzle for WMMA loads | bottleneck: Shared-memory/L1 bank and MIO pressure on B fragment loads
- dir_03: Remove the shared scratch epilogue and emit BF16 stores from registers with wider vectors | bottleneck: Epilogue LSU/MIO pressure from shared scratch traffic and scalar BF16 stores

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
