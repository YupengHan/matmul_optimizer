# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `PTX hot-band consumer-order refinement`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_085345`
- round loop: `round 59/100`
- hypothesis: `The accepted grouped_rows=8 + one-sync handoff base is already exposing the right bottleneck mix, but the remaining long scoreboard stall suggests the PTX hot-band consumer order still leaves latency on the table. A narrower lane-local consume-order tweak inside the PTX hot-band sweep should preserve the new barrier and short-scoreboard gains while trimming the remaining long scoreboard tail.`
- expected bottleneck: `Long scoreboard latency in the PTX hot-band consumer path, not the barrier or shared-memory handoff itself.`
- code locations: `src/kernels/bf16_gemm_v1.cu:741-748, src/kernels/bf16_gemm_v1.cu:753-770, src/kernels/bf16_gemm_v1.cu:1994-2006`
- risk: `A consumer-order tweak may regress the newly recovered grouped_rows=8 balance or reintroduce scoreboard pressure if it disturbs the accepted row-pair traversal too broadly.`
- metrics to re-check: `kernel time on 20260420_084915_bf16_gemm_v1_4e5579e baseline comparison, long scoreboard, short scoreboard, barrier stall, sm__sass_thread_inst_executed_op_shared`

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
