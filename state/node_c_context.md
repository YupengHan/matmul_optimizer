# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim The Remaining PTX Export Scoreboard`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_115714`
- round loop: `round 81/100`
- hypothesis: `The zero-padding export trim already recovered runtime, so the remaining gap is likely in the PTX export lifetime itself: the scratch row-pair path still carries enough address indirection and shared-memory residence to raise long-scoreboard stalls. Narrowing that export path further should lower scoreboard cost without reintroducing the DRAM or barrier inflation seen in the failed families.`
- expected bottleneck: `PTX export-lifetime latency, shared scratch residency, and address-generation overhead in the hot-band store path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:134-143, src/kernels/bf16_gemm_v1.cu:926-1044, src/kernels/bf16_gemm_v1.cu:1930-2034`
- risk: `Low to medium. The change surface is narrow and still inside the improved restored PTX baseline, but the long-scoreboard bump may already be the cheapest remaining part of the design.`
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

- no tracked dirty paths at prepare time
