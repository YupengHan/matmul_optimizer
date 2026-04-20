# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep the export-path gain and narrow the active PTX consumer-side B reuse`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_013034`
- round loop: `round 39/100`
- hypothesis: `Primary family for round 39/100: Bank Conflict plus Register Reuse plus Ps2r on the active 128x128 K16 PTX hot-band branch. Round 38 proved the padded PTX export scratch was real upside because runtime improved to 25.974272 ms, a new best custom result only 0.056383 ms behind the 25.917889 ms CUTLASS baseline. But the run still sat on top of the earlier consumer-side B-reuse changes, and the stall mix stayed awkward instead of cleanly better: tensor-active was 47.87%, barrier stayed high at 11.13%, short-scoreboard stayed high at 5.87%, and mio_throttle remained very low at 0.55%. That combination says the export-path win should be kept, but the current two-row-pair B-fragment fusion is still probably too wide for the active PTX branch. The next best move is therefore a narrower warp-local consumer fallback rather than another broad rewrite: keep the mirrored consume order and the export scratch improvement, but shorten B-fragment lifetime or reuse scope so the branch gives back some short-scoreboard and barrier cost without surrendering the mio-throttle win.`
- expected bottleneck: `Warp-local dependency chains and synchronization exposure in the active PTX consume path, where the current B-fragment reuse shape keeps feed pressure low but still leaves short-scoreboard and barrier cost too high.`
- code locations: `src/kernels/bf16_gemm_v1.cu:708-758, src/kernels/bf16_gemm_v1.cu:1936-1960, src/kernels/bf16_gemm_v1.cu:1989-1990`
- risk: `Medium. Narrowing the current reuse pattern is bounded and stays on the active PTX branch, but it can easily give back the mio-throttle win or reduce tensor issue if the fallback becomes too timid.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, launch__registers_per_thread`

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
