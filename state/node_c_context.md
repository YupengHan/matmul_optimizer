# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore accepted base, then retest finer issue granularity on the hot band`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_091130`
- round loop: `round 63/100`
- hypothesis: `The fastest path is to return to the accepted grouped_rows=8 + reversed row-pair + right-left PTX sweep + one-sync handoff base, then reduce issue granularity in the active 128x128 PTX hot-band loop. The newer accepted base likely changed the interaction enough that #pragma unroll 1 can recover scheduling slack without reintroducing the slower grouped_rows=4 locality pattern.`
- expected bottleneck: `Issue granularity and instruction pressure inside the hot-band loop, not higher-level locality. The evidence suggests grouped_rows=4 is still slower than the accepted base and also raises DRAM to 13.05, while nearby consumer/refill variants remain negative.`
- code locations: `src/kernels/bf16_gemm_v1.cu: the accepted grouped_rows=8 / reversed row-pair / right-left PTX sweep / one-sync handoff path, src/kernels/bf16_gemm_v1.cu: the active 128x128 PTX hot-band loop where the current unroll factor is set`
- risk: `Lowering unroll may expose latency if the accepted base no longer has enough ILP, but this is a bounded retest on the newest accepted base rather than a generic old-branch unroll-1 attempt.`
- metrics to re-check: `runtime versus 25.281983 ms source run, DRAM throughput, especially whether it stays below the grouped_rows=4 level, sm issue rate and any increase in scoreboard or dependency stalls, shared-memory and register pressure in the hot-band loop`

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
