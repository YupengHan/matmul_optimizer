# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 12/20` with `9` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_183726`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 12 is a continue-family move for Human idea 7 / Register reuse, not a pivot yet. The reason is measured and specific: the first outside-in RLRL traversal run immediately produced the best non-accepted result at 33.5528965 ms, recovering most of the gap from the demoted Stage branch and landing within about 0.424 ms of the accepted base. That is a much stronger reason to continue a family than the Stage family had after four rounds. At the same time, the current Idea 7 implementation clearly has secondary costs: registers/thread rose from 167 to 172, barrier stall rose from 14.30 to 16.95, and mio rose from 2.30 to 3.17. So the correct round-12 move is not to abandon Idea 7 immediately, but to make one bounded follow-up that tries to keep the long-scoreboard gain while reducing those new costs.

Human idea audit for this round:
1. Tiling (256x128 block, 64x64 warp): accept-now. This is the best higher-ceiling pivot family, but it is ranked behind Idea 7 because Idea 7 now has direct measured evidence and much lower implementation risk.
2. Coalescing Access: defer. The kernel already uses 16-byte cp.async-style wide accesses, and current evidence does not point to global-access packing as the next main limiter.
3. Data Reuse: accept-now only as already-adopted baseline behavior. Shared-memory reuse of A and B is present in both the accepted base and the current Idea 7 branch.
4. Async Copy: accept-now only as already-adopted baseline behavior. Async copy remains part of the stable hot loop, but it is not the family to prioritize next.
5. Bank Conflict: reject-for-this-round. Prior B-feed and bank-shaping experiments were negative, and the current near-hit does not show a bank-conflict-led bottleneck.
6. L2 Cache: reject-for-this-round. Nothing in the current run suggests that L2 hit ratio is the deciding limiter versus the accepted base.
7. Register Reuse: accept-now and rank first. This family has the freshest and strongest positive evidence, and it is still close enough to the accepted base to justify one bounded follow-up.
8. Pg2s: accept-now only as baseline behavior. Global-to-shared prefetch is already present and not the active decision point.
9. Ps2r: accept-now as the fallback family and rank third. It remains a credible bounded latency-hiding alternative on the same stable control surface.
10. Stage: reject-for-this-round as a primary family. Four rounds were enough to show that it changes machine behavior but plateaus far from the accepted base, so it should not regain priority here.`
- dir_01: Human idea 7 Register reuse: keep the outside-in signal, but recode it as a lower-pressure mirrored schedule | bottleneck: Warp-local issue-order pressure and codegen-induced register growth inside the 12-fragment PTX sweep, showing up as higher barrier and mio stalls even though long scoreboard improved.
- dir_02: Human idea 1 Tiling: start a true 256x128 CTA / 64x64 warp hot-band branch | bottleneck: CTA and warp tile hierarchy ceiling, where the current 64x384 hot band may be near-optimal only within a too-narrow search family.
- dir_03: Human idea 9 Ps2r: add bounded shared-to-register lookahead on the stable two-stage PTX hot loop | bottleneck: Shared-to-register latency inside the hot PTX sweep, with long scoreboard as the main symptom and tensor activity as the payoff metric.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
