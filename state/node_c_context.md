# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 9 Ps2r: full-width PTX shared-to-register lookahead inside the 12-tile sweep`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_173445`
- round loop: `round 5/20`
- hypothesis: `Mapping: this direction is the direct accept-now implementation of human idea 9, Ps2r double-buffering from shared memory to registers. The current evidence fits it best: export-side c_shared scratch shrink alone cut shared allocation from 46.592 KiB to 38.400 KiB yet still regressed, so removing export scratch by itself is not the win. The remaining stable symptom on the restored accepted base is one-block occupancy plus persistent long-scoreboard around 6.2, which points more naturally at the warp-local shared-to-register feed path. Keep the accepted 64x384 hot-band PTX kernel and unchanged 64x96 tail, but restructure ptx_wmma_accumulate_tile_set_384() so one next B fragment is prefetched from shared to registers while the current tile's mma issues. That is materially different from the rejected half-panel compute rewrite and from the low-value issue-order retightening, because the mechanism is explicit Ps2r latency hiding inside the full-width sweep.`
- expected bottleneck: `Warp-local shared-to-register latency on B-fragment consumption is the most actionable remaining underfeed source once export shrink and handoff retime have both failed to beat the accepted base.`
- code locations: `src/kernels/bf16_gemm_v1.cu:273-299, src/kernels/bf16_gemm_v1.cu:388-402, src/kernels/bf16_gemm_v1.cu:801-818, src/kernels/bf16_gemm_v1.cu:910-948`
- risk: `Medium risk. This still lives near the inner compute walk, so it can raise registers or accidentally drift toward the already-bad explicit compute family if it stops being a pure shared-to-register lookahead. It is ranked first because it is the cleanest new mechanism that stays inside the PTX mainline and matches the residual stall pattern.`
- metrics to re-check: `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, launch__registers_per_thread, launch__occupancy_limit_registers, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed, median runtime`

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
