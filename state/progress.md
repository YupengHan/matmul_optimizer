# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `d52137aeec77eeeeffce6d3af05468487e1ea98c`
- plateau counter: `0`
- round loop: `round 36/100`
- rounds remaining: `65`
- notes: `Node C build succeeded for round 36/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_010120_bf16_gemm_v1_d52137a`
- run dir: `runs/20260420_010120_bf16_gemm_v1_d52137a`
- correctness: `PASS`
- median runtime: `26.093568 ms`
- TFLOP/s: `27.862017 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_010147`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 36/100 diagnoses run `20260420_010120_bf16_gemm_v1_d52137a` at `26.093568 ms`, which is the new best custom result and confirms that the dedicated active `128x128 K16` PTX hot-band branch recovered the accepted base instead of regressing it. The important signal is not the now-small CUTLASS gap (`0.175679 ms`); it is that the recovered active branch still shows only `48.43%` tensor-active with `8.05%` barrier stall, `4.45%` `mio_throttle`, `1.67%` short-scoreboard, `1.22%` long-scoreboard, and register-limited occupancy (`launch__occupancy_limit_registers = 2`) while DRAM (`30.93%`) and L2 (`25.77%`) remain moderate. That points to feed/orchestration inside the active PTX hot band, not raw bandwidth, as the remaining ceiling on the path from `26.09 ms` toward `20 ms`.

Human-idea audit for this round: `Tiling` is rejected as the primary family because the real active `256x128 CTA / 64x64 warp` promotion already regressed badly to `31.608721 ms`, while the restored `128x128 K16` PTX branch is now the best measured custom path. `Coalescing Access` is deferred as a standalone direction because the active branch already uses wide 16-byte `cp.async` global copies in `stage_a_shared_tile_async` and `stage_b_shared_tile_async`, and the latest run is not DRAM-bound. `Data Reuse` remains accepted as an existing baseline because the branch already reuses A and B through shared memory. `Async Copy` and `Pg2s` are also accepted as the current working baseline, but broader `Stage` rewriting is rejected for now because the earlier K32 / deeper-stage active-path attempts regressed badly. `Bank Conflict` is accepted and promoted, but only as a consumer-side B-delivery rewrite without CTA repack. `L2 Cache` and grouped launch ordering are deferred because the restored active PTX branch already beat the old base without L2 becoming the dominant limiter, so another launch-order hint is not the highest-ceiling move. `Register Reuse` and `Ps2r` remain accepted and are folded directly into the recommended consumer-side B rewrite and the sequencing fallback. That is why the ranking for this round is centered entirely on the restored active PTX branch: first consumer-side B delivery and bank behavior, second export-path / `c_shared` round-trip reduction, third fixed-shape PTX sequencing cleanup without deeper stages. The target remains `20 ms`, not merely beating the `25.917889 ms` CUTLASS baseline.`
- dir_01: Rewrite active PTX hot-band B delivery at the consumer boundary without CTA repack | bottleneck: Shared-memory B-fragment delivery and consumer-side feed behavior on the active PTX hot band, especially `mio_throttle`, short-scoreboard, and bank friction that keep Tensor Cores underfed.
- dir_02: Reduce the active PTX hot-band export path and `c_shared` round-trip | bottleneck: Epilogue-side shared-memory round-trip and export overhead in the active PTX hot-band branch, especially shared-bank writes, LSU wavefront pressure, and post-compute synchronization.
- dir_03: Specialize the active PTX steady-state sequencing without adding deeper stages | bottleneck: Hot-loop orchestration overhead on the active PTX branch: CTA barriers, fixed-shape control flow, and wait-group sequencing that dilute tensor issue even when memory stalls are already low.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `0.175679 ms`, `1.006778x` slower than CUTLASS
