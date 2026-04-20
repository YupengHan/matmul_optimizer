# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep The Accepted Unroll2 K16 Base And Retime The Existing Feed Or Issue Handoff`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_081325`
- round loop: `round 52/100`
- hypothesis: `Round 47's grouped-row=8 + K16 path at 25.529328 ms remains the accepted best base. Round 48 already falsified B-fragment lookahead, round 49 already falsified K32 cadence, round 50's `unroll 1` cleaned the stall mix but was still slower, and round 51 restored the intended `grouped-row=8 + K16 + unroll2 + no-lookahead + single-scratch export` surface to 25.716736 ms, still about 0.19 ms behind the accepted best. The highest-value next move is therefore to keep the exact accepted unroll2 branch and retime only the existing K16 double-buffer handoff, `cp.async` wait or commit placement, or row-pair consume order so some of the `unroll 1` stall cleanup survives without serializing the loop again.`
- expected bottleneck: `Feed or issue cadence and K16 stage-turnover latency inside the dominant 128x128 PTX hot-band microkernel, not raw DRAM bandwidth.`
- code locations: `src/kernels/bf16_gemm_v1.cu:721-739, src/kernels/bf16_gemm_v1.cu:743-760, src/kernels/bf16_gemm_v1.cu:1949-2005`
- risk: `This is the highest-upside direction, but it can easily drift into a disguised `unroll 1` downgrade or another hidden lookahead experiment. The implementation must preserve grouped-row=8, K16 cadence, `#pragma unroll 2`, no extra-live B fragment, and the current single-scratch export path.`
- metrics to re-check: `median runtime and TFLOP/s versus the 25.529328 ms accepted base and the <20 ms user target, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, lts__throughput.avg.pct_of_peak_sustained_elapsed, launch__registers_per_thread`

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
