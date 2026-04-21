# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 9/100` with `92` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_225317`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9/100 audit: the active PTX-local micro families now look saturated on the restored grouped-rows-4 surface. Round 7's export-address cleanup produced a real new-best custom run at 24.164352 ms, but only as PASS_FLAT; round 8's control-path issue-grouping tweak then regressed slightly to 24.170400 ms, again as PASS_FLAT. The counters across those two runs barely moved: active warps stayed pinned at about 16.61-16.62, barrier stayed near 5.42-5.45, and long-scoreboard stayed near 7.24-7.26. That is enough evidence to demote another active PTX-local retime below a real family pivot. The ranking therefore recommends moving to the grouped-row non-PTX 128x128 sibling family first, keeps the sibling export-scratch trim as the strongest follow-on inside that branch, and retains one barrier/handoff fallback only as a lower-ranked active-PTX option.`
- dir_01: Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling | bottleneck: The active PTX control/export surface looks saturated; the next opportunity is preserving grouped-row locality while changing the hot-band control/export implementation family away from the PTX microkernel.
- dir_02: Trim The Grouped-Row 128x128 Sibling Export Scratch To The PTX-Style Single Stage | bottleneck: Shared export/writeback overhead on the grouped-row non-PTX 128x128 sibling, especially its heavier generic two-stage c_shared export path.
- dir_03: Steady-state Barrier / Handoff Retime | bottleneck: Residual wait-group / barrier cadence in the active PTX hot-band loop, after the currently baked handoff and export cleanups have already been absorbed.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
