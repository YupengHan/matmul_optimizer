# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Hold Grouped-Row=8 K16 Fixed And Trim PTX Export Or Operand Live Range`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_075727`
- round loop: `round 50/100`
- hypothesis: `Round 47's grouped-row=8 PTX hot band at 25.529328 ms is still the accepted best base, while round 48's B-fragment lookahead regressed to 25.759745 ms and round 49's grouped-row=8 plus K32 stage cadence collapsed further to 31.728224 ms with tensor active down to 39.98, long_scoreboard up to 6.11, and mio_throttle up to 5.81. That means the next round should not add another extra-live B fragment or another K32 cadence experiment. The narrowest new direction is to restore the accepted grouped-row=8 K16 PTX path and trim export scratch or operand live range inside that exact microkernel so the hot band can recover warp readiness without reopening the two disproved branches.`
- expected bottleneck: `Register-pressure and latency-hiding loss inside the dominant grouped-row=8 128x128 PTX hot-band microkernel, especially around export scratch and operand lifetime rather than new pipeline depth.`
- code locations: `src/kernels/bf16_gemm_v1.cu:134-142, src/kernels/bf16_gemm_v1.cu:971-1013, src/kernels/bf16_gemm_v1.cu:1989-2007`
- risk: `This is still a hot-path PTX change. A small lifetime tweak can increase register count, disturb issue ordering, or silently reintroduce the same extra-B-live behavior that already failed in round 48. The branch must stay on grouped-row=8 and K16 cadence throughout.`
- metrics to re-check: `median runtime and TFLOP/s versus the 25.529328 ms accepted base and the <20 ms user target, launch__registers_per_thread, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`

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
