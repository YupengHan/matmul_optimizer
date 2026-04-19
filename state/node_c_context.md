# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retile to a 4-warp CTA so each K-slice carries more MMA work and more resident warps`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260418_225054`
- round loop: `round 5/20`
- hypothesis: `The fixed shape hits the tensor path exactly, so the low tensor active 23.25% is not tail overhead. The current 2-warp 32x48 CTA only allows about 22 resident warps per SM (45.63% active, 48 registers/thread, 8.704 KB shared/block) and does very little math between full-block sync points, which matches the 19.10% barrier stall and leaves Tensor Cores underfed. Moving to a shape such as a 4-warp CTA that increases MMA work per staged tile should improve latency hiding and amortize the per-iteration barrier cost.`
- expected bottleneck: `Occupancy ceiling and synchronization-limited tensor-core utilization in the steady-state mainloop`
- code locations: `src/kernels/bf16_gemm_v1.cu:20-42, src/kernels/bf16_gemm_v1.cu:164-215, src/kernels/bf16_gemm_v1.cu:268-271`
- risk: `A larger CTA can increase B staging, accumulator, or epilogue state enough to raise registers/shared memory and keep the warp ceiling unchanged or worse. Tile choices that improve barrier amortization can still lose if they make the B path or store path materially heavier.`
- metrics to re-check: `median_runtime_ms, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, launch__registers_per_thread, launch__shared_mem_per_block_allocated`

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
