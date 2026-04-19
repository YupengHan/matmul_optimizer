# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retile to a 64x96 CTA so each staged B tile feeds more MMA before the next sync`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260418_233315`
- round loop: `round 9/20`
- hypothesis: `Using docs/heuristics.md explicitly, this looks like a mixed global-memory and synchronization case rather than a tail-handling problem: DRAM is 85.34%, LSU issue is 83.65%, barrier stalls are 23.45%, mio throttle is 33.49%, and Tensor Core active time is only 26.40%. The current 32x96 / 4-warp CTA does too little tensor work for each 16x96 B slice and each CTA-wide barrier. Because the fixed shape is exactly divisible by 64x96x16, doubling the CTA along M to 8 compute warps should reuse the same B tile across more output rows, increase arithmetic intensity, and put more Tensor work between sync points.`
- expected bottleneck: `Global-memory and LSU-heavy instruction mix starving Tensor Cores; the current shared-limited 7-block residency caps the kernel near 28 active warps/SM and still leaves too little math per staged K slice.`
- code locations: `src/kernels/bf16_gemm_v1.cu:20-46, src/kernels/bf16_gemm_v1.cu:163-225, src/kernels/bf16_gemm_v1.cu:288-291`
- risk: `A larger CTA can push shared memory or accumulator pressure high enough to lose occupancy or force an accompanying epilogue rewrite, so the upside only lands if registers stay near the current 48/thread and the block still sustains strong residency on SM 8.6.`
- metrics to re-check: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active (should move clearly above ~26%), dram__throughput.avg.pct_of_peak_sustained_elapsed (should stop being the ceiling), smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active and launch__occupancy_limit_shared_mem`

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

- no tracked dirty paths at prepare time
