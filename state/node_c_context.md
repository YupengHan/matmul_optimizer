# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 10 Stage: repair the 3-stage family with an explicit terminal CTA handoff before export overlay reuse`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_180512`
- round loop: `round 8/20`
- hypothesis: `Mapping: this is a continue-family move on human idea 10, Stage multi-buffering. Round 7 is too strong to throw away: registers fell from 167 to 132, barrier from 14.30 to 4.63, long-scoreboard from 6.21 to 1.27, and mio from 2.30 to 0.68. That is far larger signal than any prior family. The current failure mode looks implementation-specific instead of conceptual: the hot kernel overlays export scratch on top of b_shared via `float* c_shared = reinterpret_cast<float*>(b_shared);` and then launches shared export immediately after the final accumulate sequence, but there is no dedicated CTA-wide handoff that proves every warp is finished reading the last B stage before any warp begins writing export scratch into the overlaid storage. The best next move is therefore to keep the 3-stage branch alive and repair that terminal ownership transition explicitly.`
- expected bottleneck: `The main blocker looks like a correctness and data-handoff bug in the stage/export ownership transition, not a lack of stage-family upside.`
- code locations: `src/kernels/bf16_gemm_v1.cu:862-896, src/kernels/bf16_gemm_v1.cu:916-920, src/kernels/bf16_gemm_v1.cu:922-945, src/kernels/bf16_gemm_v1.cu:985-1009`
- risk: `Medium risk. If the supervisor suspicion is right, this is a fixable bug and the family stays live. If the runtime remains poor after correctness is restored, then the family may be winning some stalls only by starving or deferring other work. Even so, this is the highest-ceiling move with the best measured signal on the table.`
- metrics to re-check: `correctness cases passed, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, median runtime`

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
