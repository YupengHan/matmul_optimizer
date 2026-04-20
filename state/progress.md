# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `26d98195f580e02656bb7b75067c13cb4383f797`
- plateau counter: `1`
- round loop: `round 33/50`
- rounds remaining: `18`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 33/50.`

## Latest measured custom run

- run id: `20260420_003403_bf16_gemm_v1_26d9819`
- run dir: `runs/20260420_003403_bf16_gemm_v1_26d9819`
- correctness: `PASS`
- median runtime: `27.130784 ms`
- TFLOP/s: `26.796845 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_003423`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round-33 diagnosis anchored to the real active path, not the dead grouped-order knob. The latest measured run is 27.130784 ms with tensor-active 48.24%, barrier stall 8.04%, mio throttle 4.31%, DRAM throughput 31.02%, L2 throughput 26.33%, registers/thread 94, and register-limited occupancy still at 2 blocks/SM. Important correction from the main agent: the fixed-shape default launch currently calls `bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_kernel` at `src/kernels/bf16_gemm_v1.cu:1776`, while `kFixedHotBandGroupedRows` is only consumed by `bf16_gemm_v1_tensor_core_fixed_hot_band_128x128x32_kernel` at `src/kernels/bf16_gemm_v1.cu:1500-1512`. Therefore the round-32 `grouped_rows 4 -> 2` experiment did not modify the default active hot path and should not be treated as an L2-cache success/failure signal for future ranking. Human-idea audit for this round, family by family: `Tiling`: accepted only as a real default-path experiment via the existing 256x128 / 64x64 kernel, not via dead grouped-order tuning. `Coalescing Access`: rejected as a primary direction because the active path already uses 16-byte `cp.async` wide movement in `stage_a_shared_tile_async` / `stage_b_shared_tile_async`, and DRAM is far from saturated. `Data Reuse`: accepted as already present through shared-memory A/B staging, so it is not the next move by itself. `Async Copy`: accepted as a primary family because the copy primitive exists but the orchestration around commit / wait / recycle is still expensive. `Bank Conflict`: deferred as a bounded consumer-side or PTX-microkernel family; do not reintroduce CTA-level repack or extra barriers. `L2 Cache`: rejected for this round because the measured grouped_rows knob is not on the active path and L2 throughput is not the present limiter. `Register Reuse`: accepted as a secondary family, especially inside the 256x128 retile or PTX branch, but not as an isolated tiny tweak. `Pg2s`: accepted as a primary family together with `Async Copy` and `Stage`. `Ps2r`: deferred but still viable inside a more explicit consumer-side PTX path; the current 64x64 helper already has a one-step B-fragment lookahead. `Stage`: accepted as the main diagnosis family because the active hot loop still pays block-wide synchronization around every K16 recycle. Because the target is 20 ms rather than merely beating the 25.92 ms CUTLASS baseline, the ranked directions intentionally focus on actual hot-path orchestration or high-ceiling branch changes rather than small polish.`
- dir_01: Rewrite the active 128x128 K16 hot-band steady-state around Pg2s/Stage orchestration instead of dead grouped_rows tuning | bottleneck: Active hot-band feed/orchestration overhead in the K16 global-to-shared pipeline, dominated by synchronization and shared/L1/LSU delivery rather than external memory bandwidth.
- dir_02: Re-activate and retune the real 256x128 / 64x64 hot-band tiling branch on the default launch path | bottleneck: CTA-level math-per-sync ratio and latency hiding on the hot band, with the current 128x128 shape potentially under-amortizing orchestration cost.
- dir_03: Open a dedicated PTX microkernel branch for the active hot band with consumer-side B delivery and lighter export | bottleneck: Warp-consumer operand delivery and export overhead inside the active hot-band kernel after broad pipeline scheduling gains flatten out.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `1.006143 ms`, `1.038820x` slower than CUTLASS
