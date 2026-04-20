# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Port Grouped-Row Traversal Into The Active PTX 128x128 Hot Band`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_073212`
- round loop: `round 46/100`
- hypothesis: `Round 45 confirmed the register/live-range work still has signal: runtime improved from 26.955776 ms to 26.892288 ms while tensor active rose 48.05 -> 48.24, warps active rose 16.58 -> 16.68, barrier stalls fell 11.21 -> 8.48, and short scoreboard fell 5.94 -> 2.03. But the same change also pushed pressure back into the feed path: mio_throttle jumped 0.34 -> 4.26 and L2 throughput fell 30.30 -> 25.45. That makes grouped-row plus L2-friendly CTA traversal the next higher-priority route than another blind live-range squeeze. The active PTX 128x128 path still launches the hot band in simple row-major physical order, while the dormant 128x128x32 kernel already has grouped-row pid remapping; porting that traversal into the active path should improve reuse of neighboring B/L2 footprint without giving back the compute-side gains.`
- expected bottleneck: `L2 traversal and hot-band feed locality are now the limiting factor, expressed as elevated mio_throttle and weaker lts throughput after compute-side pressure was reduced.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1633-1779, src/kernels/bf16_gemm_v1.cu:1894-1994, src/kernels/bf16_gemm_v1.cu:2023-2061`
- risk: `Changing CTA traversal can easily introduce row/column ownership bugs, and the gain may be modest if the current L2 drop is dominated by per-warp shared/B-fragment behavior instead of inter-CTA ordering. It also risks helping locality in the hot band while exposing a mismatch against the residual 64x384 row-band path.`
- metrics to re-check: `runtime_ms, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, lts__throughput.avg.pct_of_peak_sustained_elapsed, gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`

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
