# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 13/20` with `8` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_184408`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 13 is a pivot-family move. Idea 7 has not fully failed, but it has now reached the practical edge of what justifies another primary round. The evidence is concrete: round 11 improved runtime to 33.5528965 ms, round 12 improved again to 33.4274559 ms, but the second step was only 0.1254406 ms and the NCU signature was effectively unchanged: tensor 36.19, active warps 16.64, barrier 16.94, long scoreboard 5.73, mio 3.15, occupancy_limit_registers 1. That means the mirrored traversal family still has signal, but only marginal signal, and it is no longer changing the machine behavior in a way that suggests a bigger win is nearby. Given the explicit 20 ms target and the policy that a high-ceiling family may run for multiple rounds, the best round-13 decision is to pivot to Human idea 1 / Tiling and treat it as a deliberate multi-round branch.

Human idea audit for this round:
1. Tiling (256x128 block, 64x64 warp): accept-now and rank first. This is the best available high-ceiling family now that Idea 7 appears near its local limit, and it is worth multi-round exploration because the older tile sweep only searched within the current 64-row CTA family.
2. Coalescing Access: defer. Wide 16-byte access is already present, and current evidence does not point to global coalescing as the next primary limiter.
3. Data Reuse: accept-now only as baseline behavior. Shared-memory reuse of A and B remains foundational, but it is not the deciding family choice this round.
4. Async Copy: accept-now only as baseline behavior. Async copy remains in the stable hot path, but not as the next primary family.
5. Bank Conflict: reject-for-this-round. Prior B-feed and bank-layout explorations were negative and the current near-hit does not present a bank-conflict-led signature.
6. L2 Cache: reject-for-this-round. Neither the accepted base nor the idea-7 branch points to L2-hit-rate as the gating issue.
7. Register Reuse: defer. This family has genuine positive evidence, but round 12 put it near stop_condition as the mainline because the second follow-up only gave marginal runtime gain with almost no NCU movement.
8. Pg2s: accept-now only as already-adopted baseline behavior. Global-to-shared prefetch exists and is not the active family decision.
9. Ps2r: accept-now as a secondary bounded alternative. It remains more credible than reopening demoted families, but its ceiling is lower than the tiling pivot.
10. Stage: reject-for-this-round as a primary family. Four rounds were enough to show that it changes machine behavior but plateaus well above the accepted base.`
- dir_01: Human idea 1 Tiling: pivot to a new 256x128 CTA / 64x64 warp hot-band branch | bottleneck: Current 64x384 hot-band hierarchy is near a family-level ceiling; the remaining gap is dominated by tile hierarchy rather than another small warp-local scheduling tweak.
- dir_02: Human idea 7 Register reuse: one final closure pass that targets the barrier and register tax directly | bottleneck: Codegen overhead from the current mirrored traversal expression, not the reuse concept itself.
- dir_03: Human idea 9 Ps2r: bounded shared-to-register lookahead on the stable two-stage PTX hot loop | bottleneck: Residual shared-to-register latency in the stable PTX hot loop, with long-scoreboard as the main symptom.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
