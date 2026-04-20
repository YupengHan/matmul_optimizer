# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 67/100` with `34` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_093804`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 67 diagnosis is anchored to run 20260420_093724_bf16_gemm_v1_1bd482e at 25.67372799 ms. The target remains under 20 ms, and the accepted best custom result is still round 58 at 24.57088089 ms on commit 4e5579ec72e9b1f05820c895c0315235d66f30cd. Key judgment for this round: fixed-K peeling is closed-negative. Round 65 already closed export traversal reversal as negative, and round 66 restored linear export order but peeled the fixed-K steady state; that only improved runtime trivially while barrier rose 5.27 -> 6.65 and long scoreboard rose 7.59 -> 14.82, so the accepted base remains grouped_rows=8 plus PTX hot-band right-left 64x64 consume order, reversed PTX compute row-pair traversal, original linear export traversal, one-sync steady-state handoff, B-first refill, and active-loop unroll 2. Audit of the human-idea families: tiling is accepted only insofar as the current PTX hot band stays on the established 64x64 warp microtile and current CTA shape, so a broader retile is rejected for this round; coalescing and wide global access are already accepted through the current 16-byte async-copy path and are not the next lever; shared-memory reuse is already accepted in the staged A/B tiles; async copy is already accepted; bank-conflict handling is accepted only through the current right-left consume order with linear export, while export traversal reversal and broader consumer-order sweeps are closed; L2 cache and launch-order locality remain open only as a within-group closure with grouped_rows fixed at 8, while grouped_rows=16, grouped_rows=4, and grouped_rows=6 are closed; register reuse Right-Left-Right-Left is already accepted in the active consume order and should not be reopened as a new sweep family; Pg2s double buffer is already accepted; Ps2r double buffer is closed for this round through the already-rejected extra-live B lookahead, K32 cadence, and warmup-order reopen family; stage and multi-buffer are accepted only as the original one-sync, B-first, unroll-2 base, while fixed-K peeling in the active PTX hot-band loop is now closed-negative. Ranking rationale: dir_01 is the best next single node_c because it restores the accepted unpeeled base and then stays tightly bounded in the PTX export helper while preserving linear export order. Dir_02 is the remaining locality family, but only as a within-group closure at grouped_rows=8. Dir_03 is the last still-open stage-family move, but it ranks last because the same region was just falsified when the steady state was peeled.`
- dir_01: Restore the accepted unpeeled base, then tighten PTX export-scratch sync and lifetime while keeping linear export order | bottleneck: PTX export scratch live-range and warp-sync/writeback overhead on the accepted hot-band base after linear export order is restored.
- dir_02: Restore the accepted unpeeled base, then try a within-group launch-order and L2 locality closure with grouped_rows fixed at 8 | bottleneck: Residual within-group launch-order and L2 locality loss on the accepted grouped_rows=8 PTX hot-band base.
- dir_03: Restore the accepted unpeeled base, then make a very narrow one-sync handoff closure without reopening A-first, K32, or extra-live staging | bottleneck: Residual one-sync handoff and refill-order overlap loss on the accepted PTX hot-band base.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
