# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 20/100` with `81` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_003535`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 20 applies the user's new strategy directly: treat sub-0.1 ms effects as noise and push the diagnosis toward more aggressive, profile-driven structural moves. The top set therefore drops the current PTX-local micro families and prioritizes 256x128 and sibling-surface branches with larger theoretical upside.`
- dir_01: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Structural latency hiding and control amortization on the hot band due to undersized effective work per scheduling decision, not just one more PTX microkernel handoff seam.
- dir_02: Port grouped-row traversal into the non-PTX 128x128 sibling | bottleneck: Surface-level control and locality inefficiency on the current PTX hot-band path rather than one more within-surface handoff detail.
- dir_03: Retune The Auxiliary 256x128 Hot-Band K-Loop Schedule | bottleneck: K-loop scheduling and latency hiding on the broader 256x128 hot-band regime rather than PTX-local handoff or export sequencing.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
