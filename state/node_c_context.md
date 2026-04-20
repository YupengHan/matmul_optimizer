# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim PTX Export Scratch On The Restored Baseline`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_114802`
- round loop: `round 80/100`
- hypothesis: `The 128x128 two-stage sibling recovered tensor activity, but the remaining gap now looks like export-path overhead: the PTX hot-band export scratch and row/quad store helpers still carry avoidable shared-memory and address-calculation cost. Reducing that footprint should cut DRAM/L2 traffic without reopening the closed promotion families.`
- expected bottleneck: `PTX epilogue export bandwidth, shared scratch lifetime, and L2 traffic in the hot-band store path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:134-143, src/kernels/bf16_gemm_v1.cu:926-1044`
- risk: `Low to medium. The change surface is narrow and still inside the restored PTX baseline family, but the upside is capped if the current slowdown is mostly environmental.`
- metrics to re-check: `median runtime, dram__throughput.avg.pct_of_peak_sustained_elapsed, lts__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, launch__occupancy_limit_registers`

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

- `src/kernels/bf16_gemm_v1.cu`
