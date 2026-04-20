# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `b11ebbb1a81c2e9c203677f3a475e95dc0a05bfb`
- plateau counter: `12`
- round loop: `round 11/20`
- rounds remaining: `10`
- notes: `Node C build succeeded for round 11/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_182615_bf16_gemm_v1_b11ebbb`
- run dir: `runs/20260419_182615_bf16_gemm_v1_b11ebbb`
- correctness: `PASS`
- median runtime: `35.803072 ms`
- TFLOP/s: `20.306063 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_182858`
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

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `6.083199 ms`, `1.234710x` slower than CUTLASS
