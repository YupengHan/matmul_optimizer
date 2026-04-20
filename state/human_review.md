# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 9/20` with `12` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `node_b_20260419_181340_round09_512448e`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9 diagnosis is a continue-family move, not a pivot away from Idea 10 / Stage. Round 8 repaired the terminal CTA handoff and kept the Stage-family signature almost intact: barrier 4.60, long scoreboard 1.21, mio 0.71, correctness 3/3. The runtime is still bad at 35.69459343 ms, so the live question is no longer whether Stage changes machine behavior; it is whether that behavior can be converted into tensor issue and occupancy. The strongest concrete reason to keep Stage primary for one more round is that the branch already dropped registers/thread from 167 to 132 and shared/block from 46.6 KB to 44.8 KB, which puts it close enough to the 128-reg cliff that a bounded follow-up could plausibly unlock 2 CTAs/SM.

Human idea audit for this round:
1. Tiling (256x128 block, 64x64 warp): reject-for-this-round. The autotune sweep in state/autotune_round18_main_tiles.md still says 64x384 is the measured sweet spot, so abandoning it now would throw away the only tile shape with repeated wins before the live Stage signal is exhausted.
2. Coalescing Access: defer as a primary family. The kernel already uses 16-byte cp.async wide accesses, so only a smaller refill-issue specialization is justified, not a rank-1 pivot.
3. Data Reuse: accept-now as baseline behavior, but not as a new standalone family. Shared A/B reuse is already the foundation of both the accepted base and the Stage branch.
4. Async Copy: accept-now as a secondary lever. The 3-stage branch is the clearest live expression of this idea, but the next round should change refill issue mechanics only if it is materially different from the earlier handoff-retime path.
5. Bank Conflict: reject-for-this-round. Prior B-feed permutations were strongly negative, and round-8 bank pressure is already below the accepted base, so bank behavior is not the missing win.
6. L2 Cache: reject-for-this-round. The current signature does not point at L2 or DRAM as the limiter.
7. Register Reuse: accept-now as a secondary ranked direction. With feed-side stalls already crushed, warp-internal reuse order is one of the few plausible remaining levers.
8. Pg2s: accept-now only as already-adopted baseline behavior. Global-to-shared double buffering is already present; the question is how to cash it out.
9. Ps2r: defer. It showed one positive run and one failed refinement, but the live Stage branch now reaches much larger stall reductions, so Ps2r is not the best primary family this round.
10. Stage: accept-now and keep primary. Correctness is fixed, the stall signature is dramatically better, and the branch is now close enough to the occupancy cliff to justify one more technically focused continuation round.`
- dir_01: Human idea 10 Stage: keep the corrected 3-stage hot band, but squeeze it under the 128-reg cliff | bottleneck: launch__occupancy_limit_registers and residual tensor underfill after overlap gains; short scoreboard is the next stall to watch once barrier, long scoreboard, and mio are already low.
- dir_02: Human idea 7 Register reuse: stage-compatible RLRL accumulator traversal inside the 12-tile PTX sweep | bottleneck: short scoreboard and warp-internal issue efficiency inside the 64x384 PTX accumulate sweep, not CTA-level feed stalls.
- dir_03: Human ideas 2 and 4 Coalescing/Async copy: specialize the 3-stage refill issue stream without changing the macro shape | bottleneck: remaining cp.async issue overhead and LSU wavefront churn inside the 3-stage refill path once the major waits are already hidden.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
