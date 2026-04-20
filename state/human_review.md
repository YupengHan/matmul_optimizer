# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 14/20` with `7` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_190126`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 14 is a continue-family move for Human idea 1 / Tiling. The measured reason is strong: the first-cut 256x128 CTA / 64x64 warp pivot improved runtime by 2.4530878 ms and established a new accepted base at 30.9743681 ms. More importantly, the raw hot-kernel machine state says the family is solving the right problem. For the new bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel, launch__registers_per_thread is 166, shared_mem_per_block_allocated is 34.304 KB, sm__pipe_tensor_cycles_active is 37.63, barrier stall is 20.76, long scoreboard is only 0.55, short scoreboard is 6.78, mio is 2.10, active warps is 16.63, and dram throughput is only 17.85. That is exactly the signature of a family worth continuing: memory scoreboard is already mostly eliminated, so the next wins should come from reducing barrier/export tax and then register/live-state tax inside the new family rather than pivoting away immediately.

Human idea audit for this round:
1. Tiling (256x128 block, 64x64 warp): accept-now and rank first. The new tiling family just produced the largest win in many rounds and clearly deserves continued multi-round exploration.
2. Coalescing Access: defer. The branch already uses wide 16-byte copies, and DRAM throughput is low, so global coalescing is not the next primary limiter.
3. Data Reuse: accept-now as a secondary lever inside the tiling family. The recommended direction uses more effective per-warp export scratch reuse rather than a new macro-tile rewrite.
4. Async Copy: accept-now only as already-working baseline behavior. Long scoreboard and DRAM throughput are low, so async copy is not the first tax to attack next.
5. Bank Conflict: accept-now as a lower-ranked local follow-up. The new 64x64 branch has a different shared-access pattern, so a narrow bank/layout tune is newly plausible even though older broad B-feed rewrites failed.
6. L2 Cache: reject-for-this-round. The current hot kernel is not L2 or DRAM bound.
7. Register Reuse: accept-now and rank second. Register/occupancy tax inside the new 64x64 warp tile is a real next bottleneck, but the export/barrier path is a more direct first target.
8. Pg2s: accept-now only as already-adopted baseline behavior. Global-to-shared prefetch is not the current gating issue.
9. Ps2r: defer. Long scoreboard is already down at 0.55 in the new family, so a Ps2r-first follow-up is not the highest-value next move.
10. Stage: reject-for-this-round as a primary family. The new tiling branch already solved the old feed starvation more effectively than the demoted Stage family did, so there is no reason to reopen it now.`
- dir_01: Human idea 1 Tiling: keep the 256x128/64x64 family, but add paired 64x64 export scratch to cut warp barrier tax | bottleneck: Warp-local export and synchronization overhead in the 256x128/64x64 kernel, now visible as high barrier stall and elevated short-scoreboard after memory starvation has already been fixed.
- dir_02: Human idea 7 Register reuse: trim 64x64 fragment live state to chase the occupancy and short-scoreboard tax | bottleneck: Register and warp-local fragment live-state pressure inside the 64x64 PTX micro-tile, limiting occupancy and contributing to short-scoreboard.
- dir_03: Human idea 5 Bank conflict: retune the 64x64 branch's shared layout and warp load pattern only | bottleneck: Shared-memory bank/load behavior inside the new 64x64 warp tile, contributing to short-scoreboard and LSU wavefront pressure.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
