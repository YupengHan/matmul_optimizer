# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 7/10` with `4` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_212205`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 7 human-idea audit against the round-6 regression: Tiling stays accepted at 256x128 CTA / 64x64 warp because the sweep already established 64x384 hot-band width as the best macro shape on this GPU; Coalescing Access, Data Reuse, Async Copy, and Pg2s stay accepted as baseline infrastructure because the correct branch already uses 16-byte cp.async staging plus shared reuse for both operands; Stage is rejected as the next move because round 6 restored correctness but regressed runtime to 30.765568 ms and left the hot-band kernel slower at about 41.45 us with registers still pinned at 167/thread and occupancy_limit_registers still 1; Bank Conflict remains accepted only in the user's strict warp-local consumer-transform form with no extra shared tile, no extra CTA barrier, and no stage-depth loss; the newly queued L2 Cache / block-order clue is promoted from deferred to active because the kernel is register-limited to one resident block, so even a modest inter-CTA cache-locality improvement is worth testing when the cheaper control-only refactor already failed; Register Reuse and Ps2r are deferred because the branch is still at 167 regs/thread. Recommended direction dir_01 therefore tests a grouped CTA mapping / block-order clue first because it is orthogonal to the failed stage refactor, cheap to implement, and easy to falsify in one round before spending more budget on riskier feed rewrites.`
- dir_01: Human idea L2 cache: grouped CTA swizzle / block-order remap for the 64x384 hot band | bottleneck: Inter-CTA locality loss at the L2/L1 boundary on the hot-band path under one-block register-limited occupancy.
- dir_02: Human idea bank-conflict follow-through: a warp-local B consumer transform with no extra shared tile or barrier | bottleneck: Warp-local shared/L1 operand delivery and bank behavior on B fragment loads in the true hot-band kernel.
- dir_03: Warp-specialized producer/consumer on the correct 256x128 hot kernel | bottleneck: All-warps staging and barrier orchestration diluting tensor issue on a one-block register-limited hot-band kernel.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
