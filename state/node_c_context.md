# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retighten PTX Hot-Band Grouping / Orchestration Window`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_160050`
- round loop: `round 6/17`
- hypothesis: `Round 5/17 closed the expanded B-shared-skew implementation: it still lost to the accepted base and, more importantly, all three correctness runs failed with runner exit code 1. That means the next move should stay on the restored accepted PTX/export base and target the remaining scoreboard cost from the hot-band orchestration boundary instead of reopening shared-layout risk. A bounded retune around `kFixedHotBandPtxGroupedRows` and the grouped-row logical mapping is the best next family because it preserves the known-correct export and copy layout while testing whether the CTA grouping itself is the leftover latency source.`
- expected bottleneck: `Long-scoreboard and barrier cost caused by PTX hot-band grouping and grouped-row orchestration.`
- code locations: `src/kernels/bf16_gemm_v1.cu:155-156, src/kernels/bf16_gemm_v1.cu:1969-1979, src/kernels/bf16_gemm_v1.cu:2096-2102`
- risk: `Medium. This remains inside the accepted PTX microkernel family and avoids the shared-layout correctness risk, but changing the grouping window can still perturb memory traffic or scheduler balance.`
- metrics to re-check: `correctness, median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
