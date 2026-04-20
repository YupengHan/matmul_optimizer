# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Rewrite active PTX hot-band B delivery at the consumer boundary without CTA repack`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_010147`
- round loop: `round 36/100`
- hypothesis: `The restored `26.093568 ms` PTX hot-band branch proves that the active `128x128 K16` surface is now the right place to keep pushing, but the branch is still far from the `20 ms` target: tensor-active is only `48.43%`, barrier is `8.05%`, and `mio_throttle` remains `4.45%` while DRAM (`30.93%`) and L2 (`25.77%`) are not saturated. The best next move is to keep the existing 16-byte `cp.async` producer path and double-buffered shared tiles intact, then rewrite only the shared-to-register B consumer path inside the active PTX microkernel: warp-local permuted or XOR swizzle, explicit `ldmatrix` or lane-remap delivery, and tighter mirrored fragment reuse so operand delivery happens at the warp boundary instead of through any new CTA-level repack. This directly accepts the human-idea families `Bank Conflict`, `Register Reuse`, and `Ps2r` on the real active path.`
- expected bottleneck: `Shared-memory B-fragment delivery and consumer-side feed behavior on the active PTX hot band, especially `mio_throttle`, short-scoreboard, and bank friction that keep Tensor Cores underfed.`
- code locations: `src/kernels/bf16_gemm_v1.cu:608, src/kernels/bf16_gemm_v1.cu:618, src/kernels/bf16_gemm_v1.cu:863, src/kernels/bf16_gemm_v1.cu:883, src/kernels/bf16_gemm_v1.cu:1741, src/kernels/bf16_gemm_v1.cu:1795`
- risk: `Medium-high risk: the change is still bounded to the active PTX branch, but a consumer-only B rewrite can silently break fragment ownership, increase register pressure, or worsen bank behavior if the new lane mapping stops matching `ptx_wmma_load_b_row` and the mirrored MMA order.`
- metrics to re-check: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, launch__occupancy_limit_registers`

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
