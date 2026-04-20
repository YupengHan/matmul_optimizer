# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 7 Register reuse: keep the outer 64x384 hot path, but serialise the inner live set into 2x192 micro-panels`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_202755`
- round loop: `round 1/10`
- hypothesis: `The current correct 64x384 PTX path is no longer barrier- or mio-limited: barrier is only 6.58%, mio throttle is 0.33%, DRAM is 17.39%, but tensor active is still only 38.58% and warps active only 16.59% with launch__occupancy_limit_registers = 1. That is a classic register-wall signature. The highest-upside next move is therefore not another feed tweak first; it is to keep the outer CTA count advantage of 64x384 while cutting the live accumulator and B-fragment set roughly in half by issuing two serial 192-column subpanels inside the same fixed peeled kernel. This preserves the proven macro shape while targeting the actual limiter that remains on the correct branch.`
- expected bottleneck: `Register pressure and resulting latency-hiding loss on the stable 64x384 PTX hot path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:PtxWmmaAccTileSet384, src/kernels/bf16_gemm_v1.cu:PtxWmmaMirroredTileIndex384, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_tile_set_384, src/kernels/bf16_gemm_v1.cu:accumulate_peeled_shared_stage_ptx, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_peeled_kernel, src/kernels/bf16_gemm_v1.cu:ptx_wmma_store_tile_pairs_384`
- risk: `Moderate. This stays on the correct branch, but it touches the hot PTX control path and can easily give back the CTA-count win if the extra serialisation adds too much steady-state overhead.`
- metrics to re-check: `correctness, median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`

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
