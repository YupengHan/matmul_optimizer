# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 10 Stage: structural pivot to a true deeper hot-band pipeline, budgeted around the export path`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_174713`
- round loop: `round 7/20`
- hypothesis: `Mapping: this direction is the round-7 primary choice for human idea 10, multi-buffer stage depth. The reason to pivot is the new combination of evidence and target: Idea 9 / Ps2r showed one real win on the exact stall it targeted, then one refinement that gave the gain back, while the overall gap to 20 ms remains massive. That says feed-path work is real, but warp-local Ps2r micro-tuning alone is unlikely to close the gap. The higher-ceiling next move is therefore a structural hot-band pipeline branch: keep the 64x384 PTX microkernel line and unchanged 64x96 tail, but redesign the hot loop around a genuine deeper global-to-shared stage plan, with export-path budget treated as an enabler rather than a standalone optimization. Concretely, the round should start by proving a shared-budget plan that can support a real extra A/B stage or equivalent stage-depth effect, instead of another two-stage retime.`
- expected bottleneck: `One-block occupancy with persistent tensor-underfeed means the kernel still lacks enough overlap depth; stage depth, not another small warp-local reorder, is the highest-ceiling remaining lever.`
- code locations: `src/kernels/bf16_gemm_v1.cu:33-67, src/kernels/bf16_gemm_v1.cu:194-208, src/kernels/bf16_gemm_v1.cu:503-529, src/kernels/bf16_gemm_v1.cu:821-854, src/kernels/bf16_gemm_v1.cu:869-905, src/kernels/bf16_gemm_v1.cu:950-956`
- risk: `High risk and explicitly a pivot. The budget may still fail to close, and a deeper pipeline can regress if it only adds synchronization. It is ranked first anyway because the user goal is 20 ms, and the current Ps2r micro-tune lane has not shown a credible path to that ceiling.`
- metrics to re-check: `launch__shared_mem_per_block_allocated, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, median runtime`

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
