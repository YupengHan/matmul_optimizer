# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 1/10` with `10` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_133418_round01_c859cd06`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `No additional human-review-only idea family is queued yet on this clean refactor branch. For round 1/10 the ranking stays tightly coupled to the live profile: test the existing 128x128x32 staged hot-band sibling first, keep the PTX wait-cadence rewrite as the higher-risk second lever, and reserve the 64x384 split rebalance as the third alternative.`
- dir_01: Promote The Existing 128x128x32 Staged Hot-Band Kernel | bottleneck: synchronization_barrier_issue and long_scoreboard latency in the current hot-band 128x128 PTX microkernel
- dir_02: Collapse The PTX Microkernel Wait-And-Sync Cadence | bottleneck: per-tile cp.async wait plus CTA barrier cadence in the PTX hot-band microkernel
- dir_03: Push More Hot-Band Rows Into The 64x384 Peeled Path | bottleneck: hot-band decomposition choice is leaving too much work on the slower 128x128 PTX hotspot instead of the best historical 384-wide family

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
