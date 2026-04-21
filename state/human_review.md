# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 36/100` with `65` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_075055`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 36 should not waste another slot on restore. The loop is already back on a clean PTX anchor, and the latest measurement at 24.175471 ms is close enough to the accepted 24.164272 ms baseline to resume real exploration. The ranking therefore moves back to live, unabsorbed families on the accepted surface: a bounded PTX control-path exploit first, the broader 256x128 low-register branch second, and a narrower steady-state handoff retime third.`
- dir_01: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual PTX hot-band control-path overhead and live-range pressure on the accepted one-K 128x128 branch.
- dir_02: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and synchronization strategy on the 256x128 hot-band path, plus correctness-sensitive writer ownership.
- dir_03: Steady-state Barrier / Handoff Retime | bottleneck: Residual wait-group and barrier cadence in the active PTX hot-band steady-state loop, especially the handoff between MMA issue completion and future-tile refill.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
