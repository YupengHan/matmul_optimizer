# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 7/9 Register reuse + Ps2r: move the 64x32 local-half live-set cut onto the true 256x128 hot-band kernel`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_203505`
- round loop: `round 2/10`
- hypothesis: `Round 1 proved that lowering register pressure on the residual 64x384 peeled kernel is not enough, because the real hotspot is still `bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel<(int)452>` at about 41.03 us with 167 registers/thread and occupancy still capped by registers. The next best move is therefore to port the previously promising 64x32 local-half schedule back onto this actual hot kernel: keep the outer CTA shape and full 256x128 coverage, but serialize each warp's 64x64 output tile into two 64x32 passes so the live B-fragment and accumulator set is cut roughly in half. This is the strongest mapping from the user's `Register Reuse`, `Ps2r`, and `Stage` ideas to the measured bottleneck, because the current failure mode is clearly latency-hiding collapse from a too-large live set rather than DRAM saturation.`
- expected bottleneck: `Register-limited occupancy and underfed tensor issue inside the 256x128 hot-band kernel. Success should lower `launch__registers_per_thread`, move `launch__occupancy_limit_registers` away from the current one-block limit, and raise `sm__warps_active` / tensor active on the dominant kernel instead of only on the peeled remainder path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:FixedHotBandTile256x128, src/kernels/bf16_gemm_v1.cu:HalfPanelIdentity64x32, src/kernels/bf16_gemm_v1.cu:stage_b_half_panel_shared_tile_async, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_tile_set_64x32, src/kernels/bf16_gemm_v1.cu:ptx_wmma_run_half_panel_control_64x32, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel`
- risk: `This is a correctness-sensitive rewrite because the old half-panel branch previously showed the right occupancy signal but failed ownership and export mapping. The main risk is recovering the register win while still writing each 64x64 warp tile to the correct global columns with no duplicated or dropped lanes.`
- metrics to re-check: `correctness_case_* max_abs_err / mean_abs_err, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed`

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
