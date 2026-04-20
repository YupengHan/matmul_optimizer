# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 68/100` with `33` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_094627`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Goal remains below 20 ms, not merely ahead of CUTLASS. The accepted best custom is still round 58 at 24.57088089 ms on commit 4e5579ec72e9b1f05820c895c0315235d66f30cd. Round 67 restored the accepted unpeeled base and removed the second export-side syncwarp in the PTX hot-band export helper. Runtime stayed flat at 25.67680073 ms, but long_scoreboard dropped sharply from 14.82 to 4.20 while barrier only eased slightly from 6.65 to 6.51. That is strong evidence that export-scratch sync and lifetime are no longer the primary runtime limiter, so the current accepted active base should now be treated as: grouped_rows=8, PTX hot-band right-left 64x64 consume order, reversed PTX compute row-pair traversal, original linear export traversal, one-sync steady-state handoff, B-first refill, active-loop unroll 2, and the trimmed export helper with only the first syncwarp retained. Closed negative branches that should not be reopened this round are: grouped_rows=16, grouped_rows=4, grouped_rows=6, export traversal reversal, fixed-K steady-state peeling, row-pair-dependent split sweep, fully mirrored sweep, A-first refill, unroll 1, the earlier CTA-level B repack, and the extra-live B lookahead, K32 cadence, and warmup-order reopenings. It is also valid to close export-side second-sync removal alone as a primary runtime lever. Human-idea audit for this round: tiling 256x128 and 64x64 is rejected as a primary family because the active-path tiling promotion and grouped_rows retunes are already measured negative; coalescing and wide global access are accepted as already implemented through the existing 16-byte async staging path and are not the next differentiator; shared-memory reuse is accepted as the working A and B base; async copy is accepted only in the current K16 two-stage B-first form; bank-conflict handling remains accepted in the current linear export path, but export-side micro-closure is now deprioritized after round 67 stayed flat; L2 cache swizzle and launch-order locality remain clearly open and are the primary family for the recommended direction as long as grouped_rows stays fixed at 8; register reuse Right-Left-Right-Left is accepted as the active PTX consume base and should not be swept again; Pg2s double buffer is accepted as already in place; Ps2r double buffer is accepted in the current hot-band helper stack and should remain fixed unless a bounded issue-order move proves worthwhile; stage and multi-buffer are accepted only as the current two-stage baseline, with the only open stage-family work now narrowed to a very small one-sync handoff closure rather than any deeper staging or peeling.`
- dir_01: Keep The Accepted PTX Base And Close Within-Group Launch-Order Locality | bottleneck: CTA issue-order locality and L2 reuse inside the active PTX hot-band mapping, not export scratch synchronization. DRAM is already low while L2 remains materially active, so the remaining upside is more likely in how grouped_rows=8 CTAs are sequenced than in another export-side micro-trim.
- dir_02: Keep The Accepted PTX Base And Test A Very Narrow One-Sync Handoff Closure | bottleneck: Steady-state handoff overhead in the active PTX hot loop, specifically the residual barrier and wait cost that remains after the export helper was trimmed. This is a synchronization-family direction, but it must stay much narrower than the already-closed fixed-K peeling branch.
- dir_03: Keep The Accepted PTX Base And Try A Bounded Issue-Order Or Locality Move | bottleneck: Warp-level issue ordering and instruction locality inside the active PTX hot-band helper stack, not the already-trimmed export helper or another grouped_rows search. The aim is to raise tensor issue efficiency within the accepted ordering semantics rather than to search new consume orders.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
