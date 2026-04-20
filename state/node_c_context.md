# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim PTX Export Syncs Inside The Single-Stage Scratch`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_154514`
- round loop: `round 2/17`
- hypothesis: `Round 1/17 proved that disturbing the recovered PTX traversal is the wrong lever: x-major traversal collapsed long-scoreboard to 4.62, but DRAM exploded to 34.29 and runtime regressed to 26.978816 ms. The next move should stay on the restored accepted base and trim the export helper itself. In the current PTX microkernel, the single-stage store recursion still executes a `__syncwarp()` for every tile column. Batching or restructuring that export path inside the same one-stage scratch should target the remaining scoreboard cost without reopening the closed paired-scratch family or sacrificing locality.`
- expected bottleneck: `PTX export-side synchronization and shared-to-global store orchestration in the hot-band epilogue.`
- code locations: `src/kernels/bf16_gemm_v1.cu:925-947, src/kernels/bf16_gemm_v1.cu:1007-1047, src/kernels/bf16_gemm_v1.cu:2025-2027`
- risk: `Medium. The change is bounded and stays on the accepted PTX baseline, but it must avoid drifting back into the already-closed paired export-lifetime design.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, correctness`

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
