# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Warp-specialize the 64x384 copy/compute pipeline on the restored base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_094909`
- round loop: `round 3/5`
- hypothesis: `Both recent human-guided families are negative evidence on top of the accepted 16a98f7 base: the two-level B repack regressed to 42.341888 ms and the phased 64x384 micro-panels regressed further to 42.673632 ms versus the accepted 37.285807 ms run. The round-2 profile did lower the hot-kernel register footprint to 80/thread and lift the register occupancy cap to 3, but barrier stall jumped to 17.31% and DRAM throughput rose to 43.78%, which points to orchestration and feed overlap rather than another B-layout or live-set rewrite. On the restored accepted base, keep the single-skew 64x384 tile and instead reduce all-warp staging overhead with a producer/consumer warp split or another lighter copy/compute overlap scheme.`
- expected bottleneck: `CTA-wide synchronization and hot-loop feed orchestration in the 64x384 K-loop.`
- code locations: `src/kernels/bf16_gemm_v1.cu:53-60 (stage-count choice tied to shared-memory budget), src/kernels/bf16_gemm_v1.cu:213-239 (A/B async staging helpers currently run by all warps), src/kernels/bf16_gemm_v1.cu:392-450 (warp mapping, cp.async commit/wait sequence, and CTA barriers in the hot loop)`
- risk: `Warp-specialized staging is more invasive than a simple schedule tweak and can starve MMA if producer warps do not hide latency cleanly.`
- metrics to re-check: `smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`

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
