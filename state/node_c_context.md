# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retune The Hot-Band Steady-State Handoff On The New Grouped-Rows-4 Base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_180213`
- round loop: `round 3/50`
- hypothesis: `Run `20260420_180146_bf16_gemm_v1_2e4dd24` is now the accepted base and the best custom result at 24.44441605 ms, beating CUTLASS while keeping the winning PTX hot-band microkernel surface intact. The grouped-rows-4 restore already proved that locality was still worth about 5.85 ms versus the regressed round-1 run, and it improved the dominant hot-band kernel itself from 32.97 ms on `da1a5bb` to 32.80 ms while dropping long scoreboard from 8.02% to 7.43%. But the hot-band kernel still dominates the profile and the remaining stall mix is still steady-state handoff shaped: tensor active is only 48.16%, barrier stall is 5.61%, and long scoreboard is still the largest hot-band stall at 7.43%. The best next move is therefore a bounded cp.async wait/commit plus consume-order retime on top of the new grouped-rows-4 base, not another broad structural pivot. That is also the best-measured family history on nearby PTX surfaces: the earlier B-first / consume / barrier retime sequence repeatedly improved similar accepted bases before this newer locality win, so the same bottleneck is still open on the stronger surface.`
- expected bottleneck: `Steady-state cp.async handoff latency and fragment-consume ordering inside the active 128x128 PTX hot-band loop, which is still leaving tensor issue on the table after the grouped-row locality fix.`
- code locations: `src/kernels/bf16_gemm_v1.cu:796-804, src/kernels/bf16_gemm_v1.cu:1076-1103, src/kernels/bf16_gemm_v1.cu:1995-2041`
- risk: `Medium. This stays inside the winning hot-band family and targets the dominant remaining stall class, but it is easy to drift into a broader stage rewrite or to undo the new grouped-rows-4 win if the handoff is widened beyond a local retime.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_metrics.csv hot-band gpu__time_duration.sum, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, dram__throughput.avg.pct_of_peak_sustained_elapsed`

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
