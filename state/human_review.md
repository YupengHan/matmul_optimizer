# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 8/100` with `93` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_224213`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 8/100 audit: the bounded PTX export-address cleanup turned the restored grouped-rows-4 PTX surface into a new best custom run at 24.164352 ms, but only by 0.016304 ms, so the current search policy still labeled the transition PASS_FLAT and did not promote the accepted base. The metric movement also says the family is nearing saturation rather than opening a fresh dominant win path: barrier improved slightly from 5.48 to 5.42, long-scoreboard ticked up from 7.17 to 7.26, and active warps stayed pinned at 16.62. The ranking therefore rotates the recommendation back to the still-open PTX control-path family, keeps one direct barrier / handoff retime alive on the same restored surface, and preserves one off-branch grouped-row export family as the fallback maintained by the round-history live-queue rehydration.`
- dir_01: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual PTX hot-band control-path overhead and scoreboard / barrier balance on the restored grouped-rows-4 PTX surface, not another export-address-only cleanup.
- dir_02: Steady-state Barrier / Handoff Retime | bottleneck: Barrier latency and stage-handoff cadence in the active PTX hot-band steady-state loop, not grouped-row mapping or epilogue bookkeeping.
- dir_03: Trim The Grouped-Row 128x128 Sibling Export Scratch To The PTX-Style Single Stage | bottleneck: Export scratch lifetime and writeback overhead on the grouped-row non-PTX 128x128 sibling path, used as an off-branch fallback if the active PTX path stalls.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
