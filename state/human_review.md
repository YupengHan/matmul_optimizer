# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 11/20` with `10` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_182858`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 11 is a pivot, not a continue-family move. Idea 10 / Stage should now be demoted and should no longer remain primary. The measured reason is straightforward: after four rounds, the family has already shown both its upside and its limit. Round 7 and round 8 proved that Stage can dramatically cut barrier, long-scoreboard, and mio. Round 9 proved that pushing the family through codegen surgery can explode catastrophically. Round 10 restored the stable Stage shape and essentially reproduced the round-8 runtime neighborhood at 35.80307198 ms. That is enough evidence to say the family is real, but stalled: it changes machine behavior without beating the accepted base, and it is nowhere near the 20 ms target.

Human idea audit for this round:
1. Tiling (256x128 block, 64x64 warp): accept-now as a structural pivot family, but not as the top recommendation. It is higher ceiling than more micro-tunes, yet also much riskier than an Idea 7 pivot.
2. Coalescing Access: defer. Wide 16-byte accesses are already present, so this is not the next main lever.
3. Data Reuse: accept-now only as already-adopted baseline behavior. Shared reuse is present in both the accepted base and the Stage branch.
4. Async Copy: accept-now only as already-adopted baseline behavior. Async staging is not what is missing after the Stage plateau.
5. Bank Conflict: reject-for-this-round. Prior B-feed and bank-shaping paths were negative, and current measured signatures do not point there.
6. L2 Cache: reject-for-this-round. Nothing in the accepted base or the Stage plateau suggests an L2-hit-ratio bottleneck is deciding the result.
7. Register Reuse: accept-now and rank first. The best remaining measured hypothesis is that warp-local fragment order and issue efficiency matter more than deeper feed overlap.
8. Pg2s: accept-now only as baseline behavior. Global-to-shared double buffering already exists and is not the current decision point.
9. Ps2r: defer. It showed earlier positive-but-insufficient signal, but the Stage family already proved that knocking down latency stalls alone is not enough to win, so Ps2r is not the strongest pivot now.
10. Stage: accept-now only as a demoted closure family. It no longer has a strong enough measured reason to remain primary after rounds 7-10.`
- dir_01: Human idea 7 Register reuse: demote Stage, restore the accepted hot-band control surface, then reorder the 12-fragment PTX sweep | bottleneck: Warp-local tensor issue efficiency and short-latency scheduling waste inside the 64x384 PTX hot sweep, not CTA-level pipeline overlap.
- dir_02: Human idea 1 Tiling: open a true 256x128 CTA and 64x64 warp hot-band branch | bottleneck: CTA and warp tile hierarchy ceiling: insufficient arithmetic density and/or poor warp-level work partitioning inside the current 64x384 family.
- dir_03: Human idea 10 Stage: keep the family only as a demoted closure experiment by collapsing the hot pipeline back toward two stages | bottleneck: Stage-depth overhead and extra CTA handoff cost that lower tensor issue even when barrier, long-scoreboard, and mio look good.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
