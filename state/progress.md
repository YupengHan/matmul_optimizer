# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `f97d68dc8a9c95ad94ac9afe3383c14343d2694e`
- plateau counter: `1`
- round loop: `round 18/50`
- rounds remaining: `33`
- notes: `Node C build succeeded for round 18/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_235839_bf16_gemm_v1_f97d68d`
- run dir: `runs/20260419_235839_bf16_gemm_v1_f97d68d`
- correctness: `PASS`
- median runtime: `30.888449 ms`
- TFLOP/s: `23.536935 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_000002`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 18: the primary accepted family is now Tiling, specifically the user-requested 256x128 block with 64x64 warp tiles, because the corrected 128x128 K16 path proved the base pipeline while the deeper 128x128x32 path hurt active warps. Async Copy, Pg2s, Ps2r, and Data Reuse remain accepted supporting mechanisms because the fixed hot-band kernels already rely on them and the next experiment should preserve that machinery. Coalescing Access and Bank Conflict are deferred because the current regressions are not showing mio- or bank-dominated signatures. Register Reuse is deferred because the latest failure mode was lower active warps rather than obvious fragment residency waste. The L2 cache / block-order clue remains deferred until the best CTA shape is established.`
- dir_01: Try the 256x128 hot-band CTA with 64x64 warp tiles on top of the proven K16 stage contract | bottleneck: CTA shape and active-warps pressure in the hot-band kernel, not deeper staging. The target is to improve warp residency and tensor issue while retaining the already-correct async-copy pipeline.
- dir_02: Keep 128x128 K16 as the base and narrow the new consume fence only at the stage handoff | bottleneck: Barrier overhead within the accepted 128x128 K16 hot-band loop.
- dir_03: Reserve the L2-friendly block-order clue for after the hot-band CTA shape stabilizes | bottleneck: Inter-CTA cache reuse rather than within-CTA tensor feed.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.287104 ms`, `1.126828x` slower than CUTLASS
