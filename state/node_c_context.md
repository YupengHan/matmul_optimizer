# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retune PTX Hot-Band Group Traversal Around The 6-Row Window`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_154129`
- round loop: `round 1/17`
- hypothesis: `The move from the regressed non-PTX sibling back to the PTX microkernel recovered DRAM and runtime, so the live opportunity is now inside the grouped-row mapping itself rather than in broad kernel-family swaps. Keeping the mid-width 6-row window but changing how `physical_pid` is translated into `logical_block_x/logical_block_y` should preserve the recovered memory locality while reducing the residual long-scoreboard cost that still trails the earlier PTX baseline.`
- expected bottleneck: `Hot-band orchestration locality and CTA traversal order inside the PTX microkernel, visible as long-scoreboard pressure with DRAM and L2 acting as guardrails.`
- code locations: `src/kernels/bf16_gemm_v1.cu:153, src/kernels/bf16_gemm_v1.cu:1946-1963, src/kernels/bf16_gemm_v1.cu:2074-2083`
- risk: `Low to medium. This stays inside the recovered PTX family and does not reopen a closed broad branch, but the upside may be limited if the remaining loss is no longer driven by CTA ordering.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, lts__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, correctness`

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
