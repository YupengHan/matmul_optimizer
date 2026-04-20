# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `f2b7c066d6bb259ec12a6d7ccfe63f381a8e8f10`
- plateau counter: `0`
- round loop: `round 53/100`
- rounds remaining: `48`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 53/100.`

## Latest measured custom run

- run id: `20260420_082007_bf16_gemm_v1_f2b7c06`
- run dir: `runs/20260420_082007_bf16_gemm_v1_f2b7c06`
- correctness: `PASS`
- median runtime: `24.895488 ms`
- TFLOP/s: `29.202859 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_082032`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 53/100 diagnosis anchored to the refreshed accepted best base from round 52: run 20260420_082007_bf16_gemm_v1_f2b7c06 at 24.895488 ms. All follow-on directions must build on this base rather than any older branch.
- Coalescing Access: no primary evidence says global coalescing is the limiter; DRAM is only 9.78, so broad load-vectorization or access-pattern rewrites are not the first move.
- Data Reuse: L2 at 30.64 with DRAM at 9.78 says reuse already exists; the reuse question is CTA grouping and reuse distance, not reopening a larger-tile or different-base search.
- Async Copy: this remains the hottest live lever. The only newly validated change was the narrow B-first cp.async issue order in the active PTX hot-band, and barrier plus MIO still dominate long scoreboard.
- Bank Conflict: current evidence does not justify a first-priority shared-layout or padding rewrite; keep that behind feed/issue retiming unless a later run shows a clear bank-conflict signature.
- L2 Cache: meaningful but not saturated, so it is a secondary tuning surface through grouped-row scheduling and locality, not a reason to chase DRAM fixes.
- Register Reuse: 200 registers per thread and an occupancy cap of 2 blocks still matter. Any next register work must trim live state on top of the round-52 base.
- Pg2s: the global-to-shared path is not waiting on raw memory latency; next Pg2s work is about handoff timing and B-first arrival order, not more stages or a K32 cadence.
- Ps2r: the PTX load or export path can still consume issue bandwidth, so export-lifetime trimming is a valid secondary direction after the B-first retiming path.
- Stage: keep the accepted K16 double buffer as the base. K32 cadence, unroll 1 as the base, and B-fragment lookahead remain closed branches.
- Target: the objective is still to drive this kernel below 20 ms, not merely to stay ahead of the CUTLASS baseline.`
- dir_01: Retune The B-First CpAsync Handoff Without Reopening K32 Or Unroll-1 | bottleneck: Async-copy feed/issue retiming in the active PTX hot-band steady state, expressed as barrier and MIO stalls rather than long scoreboard.
- dir_02: Retune PTX Hot-Band CTA Grouping For L2 Reuse On Top Of The Round-52 Base | bottleneck: L2 locality and CTA scheduling across the fixed PTX hot-band, with secondary impact on async-copy arrival regularity.
- dir_03: Trim PTX Export Or Accumulator Live State To Relieve Register-Limited Issue | bottleneck: Register pressure and PTX-side shared-to-register or register-to-shared/export lifetime, which caps active warps and leaves tensor issue underfed.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.022401 ms`, `0.960552x` slower than CUTLASS
