# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retune The Auxiliary 256x128 Hot-Band K-Loop Schedule`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_111736`
- round loop: `round 73/100`
- hypothesis: `The exact PTX round-69 surface has exhausted the bounded active-path levers that were still open, and round 72 showed export-side lifetime changes are not a win. The remaining materially different bounded family is the non-PTX 256x128 auxiliary hot-band path, whose local K-loop schedule is still conservative (`#pragma unroll 1`) despite already carrying async-copy staging and larger reuse tiles. A small local retune there, such as increasing only the steady-state unroll or lightly reshaping the per-tile loop, can test whether the larger reuse tile recovers tensor utilization without disturbing the accepted PTX base.`
- expected bottleneck: `Compute scheduling and latency hiding on the auxiliary 256x128 hot-band path, not DRAM bandwidth.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1539, src/kernels/bf16_gemm_v1.cu:1592, src/kernels/bf16_gemm_v1.cu:1606`
- risk: `Medium. This path is auxiliary rather than the current default PTX path, so upside depends on the alternative hot-band route being worth reviving; an over-aggressive unroll can also raise registers or scoreboard stalls. The PTX round-69 base should remain unchanged.`
- metrics to re-check: `runtime_ms, tflops, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, launch__registers_per_thread, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct`

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
