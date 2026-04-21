# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 34/100` with `67` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_073952`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 34 starts from a cleanly restored PTX anchor rather than from a regressed live surface. That changes the diagnosis ranking: recovery is no longer the next action. The evidence from rounds 29 through 32 still matters, though, because both 128x128 launch-bounds probes showed the same causal shape: lower registers and higher active warps alone are not enough if synchronization cost spikes. That makes PTX-local barrier/control surgery the best next move on the restored anchor, with a bounded same-surface control-path exploit as the lower-risk fallback and the 256x128 low-register transplant still reserved as the high-ceiling, high-risk branch.`
- dir_01: Trim PTX Microkernel Barriers On The Restored 128x128 Anchor | bottleneck: Barrier cadence and PTX export/control handoff inside the single-K 128x128 PTX hot-band microkernel, now that recovery is complete and the failed residency probes isolated synchronization as the limiting tax on higher occupancy.
- dir_02: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual control-path overhead and live-range pressure inside the accepted PTX one-K 128x128 hot-band branch.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and synchronization strategy on the 256x128 hot-band path, plus correctness-sensitive writer ownership.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
