# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 15/20` with `6` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_004022`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `dir_02`
- diagnosis notes: `This diagnosis incorporates the round-14 human-in-loop signal and avoids barrier/shared-B retry.`
- dir_01: Main-path explicit ldmatrix/mma.sync feed rewrite | bottleneck: Main-path operand delivery and instruction mix before tensor issue, especially the WMMA fragment-load path feeding the 64x128 CTA kernel and showing persistent smsp__warp_issue_stalled_mio_throttle_per_warp_active pressure.
- dir_02: Retile CTA and warp partition to trim per-warp N baggage | bottleneck: Per-warp fragment baggage and B-side staging pressure caused by the current CTA/warp partition, reflected in MIO throttle and possibly excess register footprint from carrying multiple N-side fragments per warp.
- dir_03: Direct-writeback epilogue that removes c_shared entirely | bottleneck: Epilogue shared-memory staging and synchronization overhead after accumulation, specifically the c_shared scratch path and warp-level syncs around accumulator writeback.

## Active direction

- selected direction: `dir_02`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
