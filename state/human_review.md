# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 15/100` with `86` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_000721`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 15/100 audit: round 14 confirmed that the round-13 regression was a single bad handoff variant, not broader source drift. The current source matches the best-known `489574e` PTX kernel file again and recovered to the 24.16-24.18 ms performance band. That lets the diagnosis filter out absorbed restore/export families and the already-rejected A-then-B handoff, then return to the strongest genuinely open active-PTX follow-on while preserving one alternate PTX surface and one orthogonal round-history fallback in the live queue.`
- dir_01: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual control-path and consume-order overhead inside the active PTX hot-band microkernel after the absorbed restore/export cleanup and the rejected handoff variant are removed from consideration.
- dir_02: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Consumer-side ordering and grouped-row locality inside the PTX hot-band microkernel under the grouped_rows=8 regime.
- dir_03: Retune The Auxiliary 256x128 Hot-Band K-Loop Schedule | bottleneck: Compute scheduling and latency hiding on the auxiliary 256x128 hot-band path, not DRAM bandwidth and not another PTX grouped-row retime.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
