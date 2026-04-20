# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `single-run` with `17` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_171921`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `All three directions stay inside the 64x384 hot-band PTX mainline and keep the 64x96 tail unchanged. Ranking is anchored on the restored accepted base 20260419_142213_bf16_gemm_v1_9bdc160 and the latest diagnosed run 20260419_171842_bf16_gemm_v1_74f163a. The explicit lesson from round 3 is that asymmetric two-stage handoff retime is not the right family to keep pushing: it recovered most of the round-2 loss by driving mio down, but it still trailed the accepted base because barrier and long-scoreboard rose. Negative evidence carried forward remains strict: no explicit half-panel mma.sync compute rewrite, no pair-compaction retry, no panelized B-load reorder, no helper/lifetime compaction retry as the main lever, and no near-neighbor handoff-retime retry. The recommended direction therefore shifts to removing real hot-path work and shared-footprint from the export side, which is both materially different and more likely to unlock the next layer of overlap.`
- dir_01: Register-first PTX pair export that shrinks hot-band c_shared scratch | bottleneck: Export-side shared traffic and scratch allocation are still taxing the hot-band kernel; they show up indirectly through LSU pressure, scoreboard exposure, and lack of real overlap headroom rather than through mio alone.
- dir_02: True third A/B stage on the hot band, funded by export-budget recovery | bottleneck: The hot-band kernel is still limited by insufficient overlap depth under one-block occupancy, not just by the precise ordering of the current two-stage handoff.
- dir_03: Full-width PTX B-fragment lookahead inside the 12-tile sweep | bottleneck: Residual long-scoreboard latency may now be dominated by the warp-local B-fragment load/use sequence inside each K-slice rather than by global stage timing.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Human ideas for future node_b

- For the next `node_b` diagnosis and later rounds, combine measured evidence with these user-provided priors instead of relying on auto-analysis alone.
- Tiling prior: prefer directions that seriously evaluate `256x128` block tiling with `64x64` warp tiling when the code path and shared/register budget make that plausible.
- Global-memory feed prior: favor wide, coalesced global-memory access patterns and non-blocking async-copy usage.
- Reuse prior: keep leaning on shared-memory reuse for both A and B, and evaluate stronger `Pg2s` double-buffer prefetching from global to shared plus `Ps2r` double-buffer prefetching from shared to registers.
- Pipeline prior: consider deeper stage or multi-buffer algorithms for global-to-shared prefetch only when the shared/register budget closes in measured code.
- Bank-conflict prior: for WMMA-oriented paths, consider padding-based shared layouts; for MMA PTX-oriented paths, consider permuted or swizzled shared layouts that eliminate bank conflicts.
- Cache prior: evaluate swizzled access modes that can improve L2 hit ratio on the fixed benchmark shape.
- Register-reuse prior: consider internal warp-tile schedules that reuse registers in a `Right Left Right Left` pattern if that can be implemented without reopening already-rejected branches.
- Diagnosis ranking rule: future `node_b` directions should explicitly say whether they align with or reject these human ideas, and why the measured evidence supports that choice.
