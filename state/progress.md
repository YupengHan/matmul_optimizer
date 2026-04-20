# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `3a888bc54495c13c7d85cfd5f98d2b64376e537f`
- plateau counter: `11`
- round loop: `round 70/100`
- rounds remaining: `31`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 70/100.`

## Latest measured custom run

- run id: `20260420_105019_bf16_gemm_v1_3a888bc`
- run dir: `runs/20260420_105019_bf16_gemm_v1_3a888bc`
- correctness: `PASS`
- median runtime: `25.499136 ms`
- TFLOP/s: `28.511532 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_105103`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Goal remains below 20 ms. The historical accepted best is still round 58 at 24.57088089 ms on commit 4e5579ec72e9b1f05820c895c0315235d66f30cd, but round 69 restored the implementation surface in src/kernels/bf16_gemm_v1.cu back to that accepted commit and re-measured only 25.49913597 ms. The only remaining diff is semantically equivalent future_tile_k arithmetic or comment shape, so the currently reproducible exact base in the present environment should be treated as about 25.50 ms, not 24.57 ms. The current exact-base metrics are tensor 48.18, dram 10.13, lts 31.11, barrier 6.41, long_scoreboard 3.98, mio 3.21, and warps_active 16.60. Round 68 snake locality is closed negative. Round 67 export-side second-sync removal is not a primary runtime lever. Fixed-K peeling, export traversal reversal, grouped_rows sweeps, A-first refill, consumer-order sweeps, and stage overexpansions remain closed negative. The active accepted surface should now be treated as: grouped_rows=8, right-left 64x64 PTX consume order, reversed PTX compute row-pair traversal, linear export traversal, one-sync steady-state handoff, B-first refill, active-loop unroll 2, accepted 256x128 unroll 1, and accepted helper shapes. Human-idea audit for this round: tiling is rejected as a search family because grouped_rows retunes and alternative active tilings are already closed negative, while the accepted 256x128 unroll-1 helper surface is simply part of the exact base; coalescing and wide global access are accepted as already implemented through 16-byte async staging and are not the next differentiator; shared-memory reuse is accepted as the working base for A and B; async copy is accepted only in the current K16 two-stage B-first form, with the recommended direction using a very narrow one-sync handoff closure rather than any refill-order change; bank-conflict handling is accepted in the current linear export path, but export-lifetime closure is now explicitly low rank after round 67 stayed flat; L2 locality is rejected for ranking this round because snake locality is already closed negative; register reuse Right-Left-Right-Left is accepted as the fixed PTX consume base and should not be swept again; Pg2s double buffer is accepted and is the primary family for the recommended one-sync handoff closure; Ps2r double buffer is accepted in the current helper stack and should remain fixed except for a bounded issue-order experiment that preserves accepted consume order; stage and multi-buffer are accepted only as the present two-stage baseline, and stage overexpansions remain closed negative.`
- dir_01: Keep The Exact Current Base And Tighten The One-Sync Handoff | bottleneck: Residual synchronization overhead in the active PTX hot-band steady-state handoff. The exact-base profile is no longer dominated by export-lifetime or large scoreboard effects, but barrier is still materially above the old round-58 snapshot, making the current one-sync handoff the best open synchronization-family target.
- dir_02: Re-Test Export Lifetime From The Exact Base, But Only As A Low-Rank Check | bottleneck: Export scratch lifetime and warp-level export synchronization as a secondary shared-memory family, not the primary runtime limiter. The evidence says this family is lower priority, but it remains one materially different fallback if the handoff closure underperforms.
- dir_03: Preserve Accepted Consume Order And Try A Bounded PTX Issue-Order Move | bottleneck: Warp-level issue packing and instruction locality inside the active PTX helper stack, not CTA-level locality or export traversal. The goal is to increase tensor issue efficiency without changing the accepted consume or row-pair order semantics.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
