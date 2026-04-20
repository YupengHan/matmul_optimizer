# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep the restored control flow and add A-side row-pair lookahead inside the 64x64 PTX microkernel`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_230713`
- round loop: `round 9/50`
- hypothesis: `The restored surface is correct again and the headline bottleneck profile still looks like compute underfeed, not DRAM saturation: tensor activity is 38.55%, short scoreboard is 6.80%, mio throttle is only 0.33%, and barrier is low. The right-left-right-left B sweep was negative, so the next human Ps2r branch should move to the A side instead of the B side. The current microkernel still loads one row pair, consumes all columns, then loads the next row pair. Keeping the next A row pair live while the current row pair is consumed is the cleanest warp-local test that matches the human Ps2r idea without touching CTA staging or control flow.`
- expected bottleneck: `Warp-local shared-to-register latency on the A-fragment path inside the 64x64 PTX microkernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_row_pairs_64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_tile_set_64x64`
- risk: `Moderate. This is warp-local and correctness-safe in shape, but it can increase live A fragments and push register pressure above the current 167/thread surface.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_metrics.csv main 256x128 hot-band gpu__time_duration.sum, runs/*/ncu_metrics.csv main 256x128 hot-band smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, runs/*/ncu_metrics.csv main 256x128 hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, launch__registers_per_thread`

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
