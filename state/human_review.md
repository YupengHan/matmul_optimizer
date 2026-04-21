# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 22/100` with `79` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_005324`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 22 treats the round-21 sibling run as a plateau-equivalent alternate surface, not as a new frontier leader. The current correct surfaces are all clustered within 0.02 ms and keep the same 16.6%-warps / 48%-tensor machine state, so the next recommendation intentionally shifts to the only historical family that ever broke that wall: the half-panel 256x128 register-reuse branch.`
- dir_01: Repair The 256x128 Half-Panel Register-Reuse Branch | bottleneck: Register-limited occupancy and oversized live state on the wide hot-band family, which the plateaued PTX and sibling surfaces are no longer moving.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: No new bottleneck is being attacked here; this is an exact recovery of the best-known implementation surface.
- dir_03: Retune The Auxiliary 256x128 Hot-Band K-Loop Schedule | bottleneck: Hot-band K-loop scheduling and latency hiding on a broader 256x128 reuse regime rather than the live-state wall on the plateaued 128x128 surfaces.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
