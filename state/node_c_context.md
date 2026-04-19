# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Rewrite shared fragment delivery to cut MIO pressure`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_002159`
- round loop: `round 13/20`
- hypothesis: `Round 12 falsified barrier frequency as the main limiter: barrier stalls dropped sharply while runtime regressed, tensor active fell to 28.43%, and MIO throttle climbed to 25.25%. The next aggressive move should target the tensor feed path itself by changing how A/B tiles are laid out in shared memory and how warps consume them so WMMA loads stop overdriving the MIO/LSU path.`
- expected bottleneck: `Shared-memory fragment delivery and MIO saturation from the current CTA-wide staging plus warp-group B skew, not CTA barrier cadence.`
- code locations: `src/kernels/bf16_gemm_v1.cu: TensorCoreTileConfig shared-layout constants, src/kernels/bf16_gemm_v1.cu: b_shared_col_from_logical, src/kernels/bf16_gemm_v1.cu: stage_a_shared_tile_async, src/kernels/bf16_gemm_v1.cu: stage_b_shared_tile_async, src/kernels/bf16_gemm_v1.cu: bf16_gemm_v1_tensor_core_kernel WMMA load path`
- risk: `High-touch layout work can silently break correctness or worsen bank behavior if the new swizzle does not match WMMA consumption exactly.`
- metrics to re-check: `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, sm__inst_executed_pipe_lsu.avg.pct_of_peak_sustained_elapsed, median runtime`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- no tracked dirty paths at prepare time
