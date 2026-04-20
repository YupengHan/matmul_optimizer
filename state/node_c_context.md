# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_02`
- direction name: `Human idea Ps2r: preload the next A row-pair while the current row-pair consumes the mirrored B stream`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260419_215936`
- round loop: `round 3/30`
- hypothesis: `The B-side mirrored streaming path plus one-fragment lookahead has already collapsed `mio_throttle` to about 0.33, but short scoreboard is still about 6.74 and each row-pair still loads its two A fragments just before issuing the four mirrored column MMAs. A smaller and more targeted follow-up than full panelization is to keep the current B-side path intact and add a one-row-pair A lookahead inside `ptx_wmma_accumulate_row_pairs_64x64`, so the next A fragments are already resident when the current row-pair finishes. That continues the Ps2r family on the operand that has not yet been prefetched within the hot-band micro-tile.`
- expected bottleneck: `Residual shared-to-register latency on the A side inside the hot-band row-pair sweep after the B side has already been partially overlapped.`
- code locations: `src/kernels/bf16_gemm_v1.cu:ptx_wmma_load_a_row, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_row_pairs_64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_tile_set_64x64`
- risk: `Moderate to high. The implementation is local, but the kernel is already near the register wall, so a second lookahead dimension can erase its own benefit if live fragments grow too much.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, launch__registers_per_thread, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed`

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
