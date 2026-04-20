# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Warp-specialized producer/consumer on top of the restored round-8 streaming B branch`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_214233`
- round loop: `round 10/10`
- hypothesis: `Round 8 showed that cleaning up the warp-local B consumer path can move runtime and feed metrics in the right direction without raising registers or shared memory. Round 9 then showed that squeezing the shared permutation harder is not the answer. The best remaining final-round bet is therefore to keep the restored round-8 streaming consumer branch and add the user's producer/consumer split on top: dedicate a small warp subset to staging and publication, while the remaining warps focus more heavily on MMA. This tests whether the residual gap is now CTA orchestration rather than raw B-fragment ordering.`
- expected bottleneck: `All-warps staging and handoff overhead after the most obvious warp-local B feed pressure has already been reduced.`
- code locations: `src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel, src/kernels/bf16_gemm_v1.cu:stage_a_shared_tile_async, src/kernels/bf16_gemm_v1.cu:stage_b_shared_tile_async`
- risk: `High but worthwhile for a final-round ceiling test. The branch is still register-limited to one resident block, so losing compute warps can erase the benefit if the producer count is wrong.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed, sm__warps_active.avg.pct_of_peak_sustained_active, launch__registers_per_thread`

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
