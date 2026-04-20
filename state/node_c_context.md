# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Tighten PTX Hot-Band Grouping For Long-Scoreboard`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_120428`
- round loop: `round 83/100`
- hypothesis: `The zero-padding export baseline is still the best current family, but the current regression suggests the remaining cost is in the PTX hot-band grouping and peel handoff rather than export padding or the two-stage feed cadence. Narrowing the grouped-row window or simplifying the peel boundary should target long-scoreboard directly without reintroducing the memory traffic that made the previous variants lose.`
- expected bottleneck: `Long-scoreboard stalls caused by hot-band orchestration, grouped-row mapping, and tail handoff in the PTX microkernel path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1181-1227, src/kernels/bf16_gemm_v1.cu:1953-1967, src/kernels/bf16_gemm_v1.cu:2079-2111`
- risk: `Medium. It stays inside the restored PTX baseline family, but the benefit depends on the scoreboard cost actually coming from orchestration rather than the core export path.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, lts__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
