# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea L2 cache clue: grouped CTA traversal for the fixed hot-band grid`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_221100`
- round loop: `round 5/30`
- hypothesis: `The current best custom branch is now correctness-stable and materially closer to CUTLASS at 29.432832 ms, but the headline micro-metrics still look almost identical to the earlier round-2 surface: tensor active about 38.63%, active warps about 16.67%, `mio_throttle` about 0.33, and L2 throughput only about 19.26%. That is a good moment to try the user-provided launch-order clue: keep the hot-band kernel logic unchanged, but remap logical CTA coordinates into a grouped traversal that clusters several block rows under the same hot-band column before advancing to the next column. If the scheduler follows block index order closely enough, this can improve B-tile reuse in L2 with very small code risk.`
- expected bottleneck: `Potential L2 locality loss from the default hot-band CTA traversal over the 60x25 grid.`
- code locations: `src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel, src/kernels/bf16_gemm_v1.cu:launch_bf16_gemm_v1`
- risk: `Low to moderate. The remap is structurally simple and does not touch the MMA pipeline, but CUDA does not guarantee issue order, so the upside may be limited or noisy.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, lts__throughput.avg.pct_of_peak_sustained_elapsed, dram__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed`

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
