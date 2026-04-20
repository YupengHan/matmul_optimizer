# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Tune PTX Hot-Band B-Shared Skew On The Accepted Export Base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_155518`
- round loop: `round 5/17`
- hypothesis: `Round 4/17 showed that retiming the PTX prefetch handoff is not the next win: long-scoreboard dropped to 5.83, but runtime still regressed to 25.98246384 ms because barrier cost rose to 6.63 without a compute-throughput gain. That closes the immediate prefetch-order family for now. The next primary move should stay on the accepted export base from round 2/17 and retune the PTX B-shared layout itself, starting with the single 16-byte skew and `b_shared_col_from_logical`, to test whether the remaining feed cost is shared-layout friction rather than copy-order timing.`
- expected bottleneck: `Shared-memory B-fragment layout friction and address-generation overhead in the PTX hot-band path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:49-53, src/kernels/bf16_gemm_v1.cu:1070-1073, src/kernels/bf16_gemm_v1.cu:2019-2022`
- risk: `Medium. The surface is still narrow and stays on the accepted PTX/export base, but changing the skew can reintroduce memory-side regressions or correctness issues if the warp-local B slices stop lining up cleanly.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, lts__throughput.avg.pct_of_peak_sustained_elapsed, correctness`

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
