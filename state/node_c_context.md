# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep the 128x128/128-thread hot-band branch but revert only the K32 mainloop back to proven K16 staging to localize correctness`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_233204`
- round loop: `round 15/50`
- hypothesis: `Round 14 finally found a high-ceiling family: the new 128x128x32 hot-band kernel cut hot-band time from about 41.62 ms to 34.98 ms and raised tensor active from about 38.13% to 45.21% and DRAM throughput from about 17.00% to 39.65%. That is too large a gain to throw away. The immediate problem is correctness, not throughput. Because the CTA shape, block size, and epilogue all changed together with the K32 stage logic, the fastest way to localize the bug is to keep the 128x128 CTA and 128-thread launch but revert only the hot-band mainloop to the simpler K16 double-buffer schedule. If that passes correctness, the error is in the K32 half-stage addressing / refill logic rather than in the new CTA shape itself.`
- expected bottleneck: `Correctness bug likely in the K32 staged mainloop bookkeeping, not in the new 128x128 warp mapping.`
- code locations: `src/kernels/bf16_gemm_v1.cu:FixedHotBandTile128x128, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_128x128x32_kernel, src/kernels/bf16_gemm_v1.cu:stage_a_shared_tile_async, src/kernels/bf16_gemm_v1.cu:stage_b_shared_tile_async, src/kernels/bf16_gemm_v1.cu:launch_bf16_gemm_v1`
- risk: `Moderate. This keeps the promising new launch shape but should reduce logic complexity materially; the main risk is that performance drops enough to hide the upside of the new CTA structure.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_metrics.csv main hot-band gpu__time_duration.sum, runs/*/ncu_metrics.csv main hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, runs/*/ncu_metrics.csv main hot-band dram__throughput.avg.pct_of_peak_sustained_elapsed, runs/*/ncu_metrics.csv main hot-band smsp__warp_issue_stalled_barrier_per_warp_active.pct`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it
- `scripts/graph.py` or `scripts/sweep_fixed_main_tiles.py` only when the direction requires minimal workflow glue

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- no tracked dirty paths at prepare time
