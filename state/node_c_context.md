# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the current best branch and re-test grouped_rows=4 under the newer launch-bounds plus unroll-2 codegen`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_002707`
- round loop: `round 31/50`
- hypothesis: `The earlier grouped-order sweep was measured before the branch adopted `launch_bounds(128, 2)` and the successful unroll-2 setting. Those two changes materially altered codegen and the scheduler profile, which means the L2 sweet spot may have shifted. The next sensible re-check is the closer neighboring grouped value, `grouped_rows=4`, on top of the current best branch rather than on the older pre-launch-bounds baseline.`
- expected bottleneck: `Cross-CTA locality under the newer compiler-guided hot-band branch, not under the earlier baseline used in the first grouped-order sweep.`
- code locations: `src/kernels/bf16_gemm_v1.cu:145, src/kernels/bf16_gemm_v1.cu:1501, src/kernels/bf16_gemm_v1.cu:1680`
- risk: `The original grouped-order result may still hold, in which case this simply gives back some of the current gain. The main reason to do it is that the surrounding codegen regime is no longer the same one we tested before.`
- metrics to re-check: `correctness pass rate on all benchmark cases, median runtime, lts__throughput.avg.pct_of_peak_sustained_elapsed, dram__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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

- no tracked dirty paths at prepare time
