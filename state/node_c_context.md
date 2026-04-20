# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Recover Accepted K16 Through Selective Feed/Issue Retiming`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_080439`
- round loop: `round 51/100`
- hypothesis: `Round 47's grouped-row=8 plus K16 hot band at 25.529328 ms remains the accepted best base. Round 50 restored that same grouped-row=8 plus K16 surface but forced the active PTX main loop to `#pragma unroll 1`, landing at 26.128896 ms, still about 0.60 ms slower. The key evidence is the stall mix: `mio_throttle 5.81 -> 3.83`, `short_scoreboard 2.82 -> 0.71`, `lts 26.91 -> 30.97`, and `barrier 9.18 -> 7.18`. That says the dominant 128x128 PTX hot band still has real feed/issue structure to mine, but the full `unroll 1` form over-serialized the loop and gave back throughput. The best next move is therefore not to keep `unroll 1` as a base, but to restore the accepted grouped-row=8 plus K16 branch and selectively retime K16 stage turnover, `cp.async` wait or commit placement, or the row-pair consume order so the cleaner stall mix survives without sacrificing total issue density.`
- expected bottleneck: `Feed/issue scheduling and K16 stage-turnover latency in the dominant grouped-row=8 128x128 PTX hot-band microkernel, not raw DRAM bandwidth.`
- code locations: `src/kernels/bf16_gemm_v1.cu:721-769, src/kernels/bf16_gemm_v1.cu:1016-1040, src/kernels/bf16_gemm_v1.cu:1949-2001`
- risk: `This is the highest-upside direction, but it can easily drift into the wrong branch. A coarse retime can recreate the throughput loss from full `unroll 1`, and a more aggressive scheduling tweak can accidentally reintroduce extra-live B behavior or higher register pressure. The implementation must stay anchored to grouped-row=8 plus K16 as the accepted base rather than promoting `unroll 1` itself.`
- metrics to re-check: `median runtime and TFLOP/s versus the 25.529328 ms accepted base and the <20 ms target, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, lts__throughput.avg.pct_of_peak_sustained_elapsed, launch__registers_per_thread`

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
