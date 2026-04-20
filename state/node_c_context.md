# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 10 Stage: revert the catastrophic __noinline__ reg-squeeze split and continue from the round-8 checkpoint`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_182158`
- round loop: `round 10/20`
- hypothesis: `Round 9 is strong negative evidence against one specific implementation strategy, not against the whole Stage family. The family-level evidence is still round 8: first correct result, barrier 4.60, long scoreboard 1.21, mio 0.71, with only a modest runtime gap versus the accepted base. Round 9 then cut registers from 132 to 126 and opened occupancy_limit_registers from 1 to 2, but tensor active collapsed from 35.12 to 3.36 while DRAM throughput jumped to 90.96 and long scoreboard to 40.26. That is not a normal miss on the occupancy cliff; it is a broken code-shape signature consistent with the new __noinline__ pipeline and export split forcing accumulator or pipeline state out of the efficient inline path and turning the hot kernel into a memory-dominated engine. The right next move is to restore the round-8 inline Stage checkpoint first and only continue Stage from there.`
- expected bottleneck: `Broken code generation and likely spill-like memory domination from the __noinline__ split, visible as extreme DRAM throughput, long scoreboard, and mio rather than useful tensor issue.`
- code locations: `src/kernels/bf16_gemm_v1.cu:505-518, src/kernels/bf16_gemm_v1.cu:915-987, src/kernels/bf16_gemm_v1.cu:990-1043`
- risk: `This spends one round on recovery rather than direct forward progress, and if the restored round-8 code shape still cannot get closer to the accepted base then the Stage family loses its strongest justification for remaining primary.`
- metrics to re-check: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed, launch__occupancy_limit_registers, median runtime`

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
