# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 21/50` with `30` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_001011`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 21: L2 Cache is now promoted to the primary family because the accepted 128x128 K16 path has stabilized and the recent CTA-local experiments either regressed or delivered only tiny gains. Stage, Async Copy, Data Reuse, Pg2s, and Ps2r remain accepted as the fixed pipeline under the current base rather than the next thing to perturb. Register Reuse is deferred after the round-19 launch-bounds failure. Tiling 256x128 remains rejected on measured evidence. Coalescing Access and Bank Conflict are still deferred because current wins and losses have not been driven mainly by those signals.`
- dir_01: Keep the accepted 128x128 K16 kernel and apply an L2-friendly grouped CTA order on the hot band | bottleneck: L2 / B-tile reuse across CTAs rather than within-CTA shared-memory orchestration.
- dir_02: Hold the accepted base fixed and continue shaving barrier work inside the K16 steady-state | bottleneck: Residual barrier overhead in the accepted K16 hot-band loop.
- dir_03: Revisit a mild compiler register hint only after the accepted base survives the L2 pass unchanged | bottleneck: Compiler allocation quality rather than CTA-local algorithm shape.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
