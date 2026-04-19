# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Stage 32-wide K macro-tiles so each sync feeds two MMA slices`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_000749`
- round loop: `round 12/20`
- hypothesis: `This fixed shape is exactly divisible by 32 along K, but the current hot path still pays cp.async commit/wait, shared-fragment setup, and CTA handoff overhead every 16-wide K step. Reblocking the main loop so one staged epoch covers two 16x16x16 MMA slices should increase tensor work per scalar/LSU episode, reduce barrier frequency, and raise tensor issue without repeating the round-11 producer/consumer register blow-up.`
- expected bottleneck: `Tensor-core underfeed from too little MMA per staging/synchronization episode in the fixed-shape main loop.`
- code locations: `src/kernels/bf16_gemm_v1.cu:27-48, src/kernels/bf16_gemm_v1.cu:191-255, src/kernels/bf16_gemm_v1.cu:307-320`
- risk: `High. A 32-wide macro-step can raise shared-memory footprint and live fragment state enough to erase the gain if registers or residency move the wrong way.`
- metrics to re-check: `median_runtime_ms, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, launch__registers_per_thread, launch__shared_mem_per_block_allocated`

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
