# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Re-enter The PTX Hot-Band Path With A Mid-Width Grouping Control`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_152858`
- round loop: `single-run`
- hypothesis: `The regression is dominated by falling off the PTX hot-band microkernel and its single-stage export-scratch path, not by the narrower grouped-row value alone. Restoring the PTX launch/store path while testing a bounded middle grouping such as 6 rows should keep DRAM near the 25.643007 ms active baseline and let the grouped-row idea be measured on the intended PTX baseline instead of on the higher-traffic non-PTX sibling.`
- expected bottleneck: `Long-scoreboard in the PTX hot-band kernel, with DRAM and L2 locality acting as guardrails while the grouped-row mapping is re-isolated.`
- code locations: `src/kernels/bf16_gemm_v1.cu:153, src/kernels/bf16_gemm_v1.cu:1934-2028, src/kernels/bf16_gemm_v1.cu:2076-2092`
- risk: `Low to medium. This is close to the best active family and directly addresses the confounding variable, but the upside may be small if grouped-row width was never the real limiter once the PTX path is restored.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, lts__throughput.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, launch__registers_per_thread`

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
