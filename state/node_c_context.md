# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retune the tensor tile so each warp does more MMA work per shared-memory feed`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260418_222017`
- round loop: `round 2/20`
- hypothesis: `The 32x32 CTA uses only 2 warps and each warp consumes 1 A fragment plus 2 B fragments for just 2 MMA ops per K-slice. After the 16-byte async-copy change, global delivery improved, but the kernel is still dominated by shared-memory issue pressure (`smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct = 42.83`) and weak residency (`sm__warps_active.avg.pct_of_peak_sustained_active = 45.70`). A tile retune that increases math per warp, starting with a wider N footprint and only then adding more warps if registers stay reasonable, should convert the faster staging path into higher tensor utilization.`
- expected bottleneck: `Shared-memory / fragment-load issue pressure with too little MMA work per warp and too few ready warps to hide it.`
- code locations: `src/kernels/bf16_gemm_v1.cu:16-35, src/kernels/bf16_gemm_v1.cu:149-228, src/kernels/bf16_gemm_v1.cu:261-264`
- risk: `Moderate. More output tiles per warp or a larger CTA can raise accumulator pressure, registers, and shared-memory footprint enough to erase the gain if occupancy collapses or the store path becomes awkward.`
- metrics to re-check: `median runtime, TFLOP/s, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, launch__registers_per_thread, launch__shared_mem_per_block_allocated`

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

- `src/kernels/bf16_gemm_v1.cu`
