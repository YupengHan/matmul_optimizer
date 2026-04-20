# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore accepted base, then retime refill issue order`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_090007`
- round loop: `round 61/100`
- hypothesis: `Anchor on the latest measured run 20260420_085928_bf16_gemm_v1_9ee9b48 at 25.821696 ms, restore the accepted grouped_rows=8 base with reversed PTX row-pair traversal, right-left PTX column sweep, and the one-sync wait_group_0 handoff, then try a narrow steady-state refill issue-order retime inside that accepted base. The mirrored-sweep experiment already reduced long scoreboard to 4.48 but still regressed badly, so consumer ordering is no longer the best next lever.`
- expected bottleneck: `Refill issue ordering after the accepted one-sync handoff, not the consumer sweep order itself.`
- code locations: `src/kernels/bf16_gemm_v1.cu:737-770, src/kernels/bf16_gemm_v1.cu:1411-1425, src/kernels/bf16_gemm_v1.cu:1992-2006`
- risk: `Low-to-moderate: if the accepted base is not fully restored first, a refill retime can confound the signal and drift back into the rejected mirrored or split-sweep paths.`
- metrics to re-check: `kernel time vs 25.821696 ms, long scoreboard, sm efficiency, branch divergence, shared-memory load/store balance`

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
