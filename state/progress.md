# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `8bbe00147480e0c3391ae212384db1411cc96d80`
- plateau counter: `3`
- round loop: `round 35/100`
- rounds remaining: `66`
- notes: `Node C build succeeded for round 35/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_005216_bf16_gemm_v1_8bbe001`
- run dir: `runs/20260420_005216_bf16_gemm_v1_8bbe001`
- correctness: `PASS`
- median runtime: `31.608721 ms`
- TFLOP/s: `23.000596 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_005302`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 35/100 diagnoses run `20260420_005216_bf16_gemm_v1_8bbe001` at `31.608721 ms`, which promoted the real `256x128 CTA / 64x64 warp` hot-band branch onto the default path. Against the accepted best run `20260420_002759_bf16_gemm_v1_1b9dbe3` at `26.924031 ms`, the active-path regression is clear: tensor-active dropped from `48.56%` to `36.60%`, short-scoreboard rose from `1.70%` to `6.74%`, long-scoreboard rose from `1.31%` to `2.47%`, barrier stayed elevated (`8.13%` -> `8.46%`), and both DRAM (`31.35%` -> `16.44%`) and L2 (`26.48%` -> `18.38%`) moved down. That rejects more `Tiling` exploration on this branch, just as round 33 already rejected the `128x128x32` `Async Copy/Pg2s/Stage` rewrite.

Human-idea audit for this round: `Tiling` is rejected as the primary family because both the true `256x128/64x64` promotion and the earlier K32 active-path rewrite regressed badly versus the accepted base. `Coalescing Access` is deferred because the hot kernels already use 16-byte `cp.async` loads and the latest run is not DRAM-bound. `Data Reuse` remains accepted as a baseline property of the restored base, but it is not the next differentiator. `Async Copy`, `Pg2s`, and broader `Stage` rewriting are deferred or rejected as primary moves for now because the K32/deeper-stage branch already lost on the real active path. `L2 Cache` is also deferred as a secondary clue only, not the main lever, because grouped ordering alone is not enough to explain a path from 26.9 ms to 20 ms. The families still accepted and promoted are `Bank Conflict`, `Register Reuse`, and `Ps2r`, plus the export-side shared-memory budget issue. That is why the ranking now shifts to the remaining high-ceiling active-path ideas: a PTX microkernel first, a narrower consumer-side B-delivery rewrite second, and export/`c_shared` cleanup third. Every active-path direction above assumes restoring the accepted `128x128 K16` base before experimentation, because the goal remains `20 ms`, not merely beating CUTLASS.`
- dir_01: Restore the 26.924 ms 128x128 K16 base and open an active hot-band PTX microkernel branch | bottleneck: Tensor Core under-utilization caused by active hot-band consumer feed, fragment scheduling, and export overhead on the current accepted path; this is the remaining family with enough upside to move from 26.9 ms toward the 20 ms target.
- dir_02: Restore the accepted K16 base and do a consumer-side B-delivery rewrite without CTA repack | bottleneck: Shared-memory consumer delivery of B fragments on the accepted active hot band, especially short-scoreboard and bank behavior that keep tensor issue from rising even when DRAM is not busy.
- dir_03: Restore the accepted K16 base and trim the hot-band export path plus `c_shared` round-trip | bottleneck: Export-path shared-memory overhead and epilogue-side synchronization that dilute tensor issue on the active hot band even when the main loop is otherwise healthy.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `1.006143 ms`, `1.038820x` slower than CUTLASS
