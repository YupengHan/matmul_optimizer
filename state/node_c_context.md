# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `64x192 main + 64x128 middle + 64x96 tail fixed split`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_010436`
- round loop: `round 17/20`
- hypothesis: `Build directly on the successful widened-main result by replacing the current 64x160 hot band with a 64x192 main launch over the first 7296 columns, then a 64x128 middle launch over the next 384 columns, and finally the existing 64x96 tail over the last 96 columns. That reduces dominant-region CTA count from 48 to 38 while keeping cleanup on already shape-friendly tiles, which should improve tensor issue density and trim barrier/MIO overhead without pushing DRAM much past the current 51.22%.`
- expected bottleneck: `The main bottleneck should remain tensor-core under-utilization in the dominant hot band, with barrier and MIO throttle caused by too many medium-width CTAs rather than raw DRAM bandwidth.`
- code locations: `src/kernels/bf16_gemm_v1.cu:52-81 (add a TensorCoreTile192 alias plus fixed-shape split constants/static_assert coverage for 7296 + 384 + 96 columns), src/kernels/bf16_gemm_v1.cu:133-157 (reuse the async-copy staging helpers with the widened B-tile geometry and validate 16-byte alignment assumptions), src/kernels/bf16_gemm_v1.cu:322-335 (rewrite the fixed-shape launch branch to issue 64x192 main, 64x128 middle, then 64x96 tail)`
- risk: `A 64x192 tile increases the B tile footprint and per-CTA fragment pressure. If register/shared usage climbs enough to cut active warps materially below the current 65.67% or amplify barrier stalls, the fewer CTAs will not offset the heavier block.`
- metrics to re-check: `end-to-end median runtime versus 42.56455994 ms, main-kernel sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, main-kernel sm__warps_active.avg.pct_of_peak_sustained_active, main-kernel smsp__warp_issue_stalled_barrier_per_warp_active.pct, main-kernel smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, main-kernel launch__registers_per_thread and launch__shared_mem_per_block_allocated`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- `src/kernels/bf16_gemm_v1.cu`
