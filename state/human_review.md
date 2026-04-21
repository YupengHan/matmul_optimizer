# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 11/100` with `90` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_233235`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 11/100 audit: round 10 exposed a search-memory hygiene issue that the loop now has to account for explicitly. The nominally top-ranked sibling export-trim family is already absorbed in the current source, so repeating it would only create a fake node_c round; after switching to an approved PTX control fallback, the latest measured run still regressed to 24.19046402 ms while the headline signature stayed effectively unchanged at 16.61 active warps, 5.46 barrier, and 7.24 long-scoreboard. This diagnosis therefore filters absorbed or already-baked families out of the top ranks and reorders only the still-actionable current-source deltas. The recommendation moves to the steady-state barrier/handoff retime because it is the strongest open frontier family that is both unabsorbed and still aligned with the latest flat scheduler signature.`
- dir_01: Steady-state Barrier / Handoff Retime | bottleneck: Residual wait-group and barrier cadence in the PTX hot-band steady-state loop, especially the handoff between the current stage's MMA issue and the future-tile refill sequence.
- dir_02: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Consumer-side ordering and grouped-row locality inside the PTX hot-band microkernel, especially around the grouped CTA mapping and export-handoff behavior.
- dir_03: Retune Hot-Band CTA Traversal On The 128x128 PTX Grid | bottleneck: Inter-CTA locality and traversal efficiency on the current 128x128 PTX hot-band grid rather than another inner-loop scheduler issue.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
