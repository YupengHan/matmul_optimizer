# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 12/50` with `39` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_231606`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 12/50 absorbs a strong negative result from the half-CTA Pg2s experiment. The hot-band kernel regressed badly, so the next staging-family move should deepen overlap by reallocating shared-memory budget instead of reducing the number of copy-issuing threads. The untried secondary family remains a consumer-side B swizzle that does not add CTA-level repacking.`
- dir_01: Restore the accepted-correct hot-band surface and trade paired c_shared scratch for a 3-stage A/B pipeline | bottleneck: Tensor under-utilization from a too-shallow hot-band mainloop pipeline rather than pure DRAM bandwidth.
- dir_02: Restore the accepted surface and try a light consumer-side B XOR/interleaved swizzle with no extra shared footprint | bottleneck: Shared-memory bank behavior and operand delivery on the hot-band B consumer path.
- dir_03: Restore the accepted-correct implementation surface before any new experiment | bottleneck: Not a bottleneck attack; this is the reset path that preserves signal quality for later rounds.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
