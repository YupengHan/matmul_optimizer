# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the accepted-correct control flow and switch the 64x64 column sweep to explicit right-left-right-left order`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_230227`
- round loop: `round 7/50`
- hypothesis: `Three rounds proved that the peeled steady-state control idea is fast but not quickly repairable. The next high-signal move is to separate correctness from warp scheduling again: restore the proven generic hot-band loop, keep the shared PTX hot-band family, and apply the user's warp-local register-reuse idea directly by changing the 64x64 B-column sweep from the current left-right mirrored order to an explicit right-left-right-left order. That gives one clean experiment on the accepted-correct surface and tells us whether warp-local operand order is the real remaining headroom.`
- expected bottleneck: `Per-warp operand delivery and register reuse inside the 64x64 PTX hot-band microkernel rather than CTA-level pipeline control.`
- code locations: `src/kernels/bf16_gemm_v1.cu:PtxWmmaMirroredTileIndex64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_load_col_fragment_64x64, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_64x64_kernel`
- risk: `Moderate. The control-flow restore is straightforward, and the new behavior is isolated to warp-local fragment order on the proven correct surface.`
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

- `src/kernels/bf16_gemm_v1.cu`
