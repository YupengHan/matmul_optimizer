# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the accepted 128x128 K16 base and scope the consume fence only to real stage overwrites`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_000825`
- round loop: `round 20/50`
- hypothesis: `Round 19 showed that aggressive launch-bounds pressure is not a viable path on this kernel: runtime doubled, tensor active collapsed, and memory stalls exploded. The next move should therefore be a strict return to the accepted 29.20 ms base, followed by the smallest possible Stage-family refinement. The most bounded variant is to keep the proven 128x128 K16 kernel, remove the launch-bounds hint, and only execute the added consume-side CTA fence on iterations that actually overwrite the current shared stage. That preserves the correctness fix while trimming barrier work on the final tiles where no future overwrite happens.`
- expected bottleneck: `Barrier / orchestration overhead in the accepted 128x128 K16 hot-band loop, with no increase in shared footprint or register pressure.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1610, src/kernels/bf16_gemm_v1.cu:1678, src/kernels/bf16_gemm_v1.cu:1683, src/kernels/bf16_gemm_v1.cu:1757`
- risk: `The upside is modest because the fence only disappears on the tail of the fixed K loop. The main risk is accidentally weakening the correctness guard and reopening the round-15 race.`
- metrics to re-check: `correctness pass rate on all benchmark cases, median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`

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
