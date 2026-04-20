# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea L2 cache: grouped CTA swizzle / block-order remap for the 64x384 hot band`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_212205`
- round loop: `round 7/10`
- hypothesis: `The accepted 64x384 outer shape is already the measured sweet spot, but round 6 showed that simplifying only the steady-state control path does not move the wall: runtime regressed, hot-band time rose to about 41.45 us, tensor active stayed near 38%, and the kernel is still register-limited to one resident block. In that low-occupancy regime, inter-CTA cache locality matters more because the machine has less warp-level latency hiding. A Triton-style grouped mapping from physical `blockIdx` to logical hot-band tiles can keep the same B slab resident across several neighboring M tiles, or keep adjacent A tiles hotter across grouped N tiles, without changing the kernel math, shared footprint, or register footprint. This makes the user's L2 block-order clue the cheapest orthogonal next experiment on the correct branch.`
- expected bottleneck: `Inter-CTA locality loss at the L2/L1 boundary on the hot-band path under one-block register-limited occupancy.`
- code locations: `src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_peeled_kernel, src/kernels/bf16_gemm_v1.cu:launch_bf16_gemm_v1`
- risk: `Moderate but contained. CUDA does not guarantee launch order, so the gain has to come from a logical CTA remap rather than a scheduler promise. A grouped order can improve B reuse while slightly worsening A reuse, and the hot-band / peeled split must stay exact.`
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
