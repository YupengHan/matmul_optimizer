# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 22/50` with `29` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_001157`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 22: L2 Cache remains the primary family because it just produced the best custom runtime so far without perturbing the working CTA-local pipeline. Stage, Async Copy, Data Reuse, Pg2s, and Ps2r remain accepted fixed infrastructure rather than the next tuning knob. Register Reuse is still deferred after the launch-bounds failure. Tiling 256x128 stays rejected on measured evidence. Coalescing Access and Bank Conflict remain deferred because the current improvement signal came from CTA ordering, not those metrics.`
- dir_01: Keep the grouped CTA-order remap and increase the hot-band row-group size to deepen B-tile reuse | bottleneck: Cross-CTA B reuse / L2 locality rather than CTA-local staging or occupancy.
- dir_02: Keep the grouped-order remap but reduce the row-group size to check whether the current win is already over-grouped | bottleneck: Cache-locality tuning of the grouped CTA traversal.
- dir_03: Hold the grouped-order base fixed and return to conservative K16 barrier trimming | bottleneck: Residual barrier overhead inside the accepted grouped-order K16 kernel.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
