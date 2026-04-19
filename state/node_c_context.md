# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Tile384 epilogue budget for overlap`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260419_125849`
- round loop: `round 5/5`
- hypothesis: `Keep the measured 64x384 hot band, but treat the c_shared epilogue/export path as the easiest budget source for the main loop rather than as a standalone store path. On the restored base, the hot peeled kernel still allocates 46.592 KB shared per block and spends a float c_shared round-trip at src/kernels/bf16_gemm_v1.cu:570-574 and :668-699 while headline tensor active stays only 35.06 and mio throttle stays 35.64. Compressing or lightening that c_shared path should be pursued only if the saved shared-memory budget can be reinvested into a deeper A/B prefetch window or otherwise wider hot-path overlap at :599-666. The success condition is not merely fewer export stores; it is buying overlap budget back for the tensor loop.`
- expected bottleneck: `The limiting factor is overlap budget inside the 64x384 peeled kernel: shared-memory allocation and epilogue round-trip pressure leave the hot loop underfed, which shows up as persistent mio throttle and only middling tensor activity despite low DRAM pressure.`
- code locations: `src/kernels/bf16_gemm_v1.cu:41-60, src/kernels/bf16_gemm_v1.cu:570-574, src/kernels/bf16_gemm_v1.cu:599-666, src/kernels/bf16_gemm_v1.cu:668-699`
- risk: `If the c_shared savings are too small to fund a real overlap change, this devolves into epilogue-only churn with low upside. Additional CTA-wide B repacks, producer splits, or extra synchronization would violate the evidence from rounds 1, 3, and 4 and should stay out of scope.`
- metrics to re-check: `launch__shared_mem_per_block_allocated, l1tex__data_bank_writes.avg.pct_of_peak_sustained_elapsed, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, median runtime`

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
