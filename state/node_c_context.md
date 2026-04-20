# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Fast Auxiliary 256x128 Default Hot-Band Path`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_113413`
- round loop: `round 76/100`
- hypothesis: `The round-75 64x384 default promotion family is now closed-negative for this round: runtime regressed to 33.59487915 ms, tensor activity fell to 36.06, barrier stalled to 16.62, DRAM throughput jumped to 54.20, and register occupancy fell to 1. The strongest next move is to undo that wide-tile default and restore the fast auxiliary 256x128 hot-band path as the default route, because that family already proved materially better than the 64x384 promotion while staying distinct from the PTX microkernel path. This should bring the benchmark back toward the prior fast regime while keeping the hot band on the more reuse-friendly 256x128 schedule instead of the memory-heavy 384-wide path.`
- expected bottleneck: `The 64x384 promotion is exposing DRAM overfetch and barrier amplification rather than compute throughput, so the fix is to return to the lower-overhead 256x128 schedule and recover tensor utilization.`
- code locations: `src/kernels/bf16_gemm_v1.cu:152-159, src/kernels/bf16_gemm_v1.cu:1181-1227, src/kernels/bf16_gemm_v1.cu:1561-1606, src/kernels/bf16_gemm_v1.cu:2064-2105`
- risk: `Medium. This is the most grounded recovery path because it directly reverses the failed 64x384 default and returns to a previously faster distinct family, but it still has to preserve correctness and avoid reintroducing the wide-tile default through the launch gate.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed, dram__throughput.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_barrier_per_warp_active.pct, launch__occupancy_limit_registers`

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
