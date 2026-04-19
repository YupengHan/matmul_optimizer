# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Main-path explicit ldmatrix/mma.sync feed rewrite`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_004022`
- round loop: `round 15/20`
- hypothesis: `Round 14 showed the human epilogue vectorization is safe and near-neutral on the hot path, while MIO throttle stayed at roughly 41.7%. The next real lever is to rewrite the 64x128 main-path feed pipeline so the WMMA fragment-load sequence is replaced by an explicit shared-to-register ldmatrix / mma.sync flow, keeping the accepted round-14 epilogue behavior intact.`
- expected bottleneck: `Main-path operand delivery and instruction mix before tensor issue, especially the WMMA fragment-load path feeding the 64x128 CTA kernel and showing persistent smsp__warp_issue_stalled_mio_throttle_per_warp_active pressure.`
- code locations: `src/kernels/bf16_gemm_v1.cu: TensorCoreTile128 tile/layout constants, especially the main-path B shared layout and warp-group shape, src/kernels/bf16_gemm_v1.cu: bf16_gemm_v1_tensor_core_kernel<TensorCoreTile128> K-loop around wmma::load_matrix_sync and wmma::mma_sync, src/kernels/bf16_gemm_v1.cu: existing vectorized epilogue block after accumulator writeback, which should be preserved unless a glue fix is strictly required`
- risk: `Highest implementation complexity of the three. Inline PTX register packing, lane mapping, and shared-layout assumptions can break correctness or inflate register pressure; the safe tail path and round-14 epilogue should remain stable to contain blast radius.`
- metrics to re-check: `median runtime, TFLOP/s, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, launch__occupancy_limit_registers`

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
