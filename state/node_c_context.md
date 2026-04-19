# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `PTX hot-band microkernel branch with unchanged 64x96 tail`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260419_130817`
- round loop: `round 1/5`
- hypothesis: `The accepted 64x384 base still shows only middling tensor activity at 34.81 with mio throttle at 35.62 and DRAM throughput only 28.98, so the hot band still looks feed/orchestration limited rather than bandwidth limited. The current hot kernel is still routed through the WMMA control surface at src/kernels/bf16_gemm_v1.cu:534-699, which hides fragment residency, load order, lane mapping, and export choices behind wmma::load_matrix_sync, wmma::mma_sync, and wmma::store_matrix_sync. Open an independent 64x384-only branch that keeps the 64x96 tail path untouched but extracts the hot band into an explicit PTX microkernel using ldmatrix, mma.sync, and a controllable register/export path so later rounds can refine the same microkernel instead of continuing WMMA micro-tunes.`
- expected bottleneck: `The dominant limiter is the WMMA hot-band control surface itself: it constrains fragment lifetime and instruction ordering, which keeps tensor issue diluted by feed/orchestration overhead even though the macro tile and tail split are already well chosen.`
- code locations: `src/kernels/bf16_gemm_v1.cu:231-263, src/kernels/bf16_gemm_v1.cu:278-282, src/kernels/bf16_gemm_v1.cu:319-365, src/kernels/bf16_gemm_v1.cu:534-699, src/kernels/bf16_gemm_v1.cu:728-760`
- risk: `This is the largest implementation step in the branch: explicit lane mapping, ldmatrix addressing, and mma.sync accumulator layout can break correctness or push registers above the current 128/thread budget. If the first PTX cut expands live state too aggressively, occupancy can collapse the same way earlier high-complexity feed rewrites did.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, launch__registers_per_thread, launch__occupancy_limit_registers`

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
