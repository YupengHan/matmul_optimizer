# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `8c2a778a7ff52bec9a777c667ae4be6ac96ce39f`
- plateau counter: `7`
- round loop: `round 66/100`
- rounds remaining: `35`
- notes: `Node C build succeeded for round 66/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_092926_bf16_gemm_v1_8c2a778`
- run dir: `runs/20260420_092926_bf16_gemm_v1_8c2a778`
- correctness: `PASS`
- median runtime: `25.692160 ms`
- TFLOP/s: `28.297326 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_093003`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Goal remains sub-20 ms, not merely staying ahead of CUTLASS. The accepted best custom is still round 58 at 24.57088089 ms on commit 4e5579ec72e9b1f05820c895c0315235d66f30cd. Round 65 should be read as a negative closure on export-order reversal: it restored grouped_rows=8 but changed the PTX hot-band export traversal to higher-row-pair-first, and runtime regressed to 25.69215965 ms. Compared with round 64, headline metrics improved slightly, with dram 11.58 -> 10.39, barrier 5.35 -> 5.27, and long_scoreboard 7.69 -> 7.59, yet total time still worsened. That is strong evidence that the export-order reversal itself is negative and should be closed, while grouped_rows=8 remains the accepted locality base. The accepted active base that all three directions assume is: grouped_rows=8, PTX hot-band right-left 64x64 consume order, reversed PTX compute row-pair traversal, original linear export traversal, one-sync steady-state handoff, B-first refill, and active-loop unroll 2. Closed negative branches that should not be reopened this round are: grouped_rows=16, grouped_rows=4, grouped_rows=6, export traversal reversal, row-pair-dependent split sweep, fully mirrored sweep, A-first refill, unroll 1, earlier CTA-level B repack, and the extra-live B lookahead, K32 cadence, and warmup-order reopenings. Human-idea audit for this round: tiling 256x128/64x64 is rejected as a primary direction because the real active-path tiling promotion already regressed and grouped_rows retunes around the current PTX base are now closed; coalescing and wide global access are accepted as already implemented through 16-byte async copy and do not explain the remaining gap; shared-memory reuse is accepted as the working PTX base for A and B tiles; async copy is accepted only in the current K16 two-stage B-first form, while deeper or alternative refill order variants are rejected for this round; bank-conflict handling remains open only through careful PTX export-scratch closure inside the restored linear export order, not through another export traversal sweep; L2 cache swizzle or launch-order locality remains open only as an within-group order experiment with grouped_rows fixed at 8; register reuse Right-Left-Right-Left is accepted as the active PTX consume base and should not be retuned this round; Pg2s double buffer is accepted as already in place; Ps2r double buffer is accepted in the current PTX hot-band consume path and should remain fixed while other families are tested; stage and multi-buffer are accepted only as the current two-stage baseline, with the recommended direction using fixed-shape prologue, steady-state, and epilogue peeling to reduce control overhead rather than adding more stages.`
- dir_01: Restore Linear PTX Export Order, Then Peel The Fixed-K Steady State | bottleneck: Hot-loop orchestration in the active PTX 128x128 K16 kernel, especially barrier plus long_scoreboard overhead from the generic fixed-K loop handoff rather than raw DRAM bandwidth or a new tiling problem. The metrics still show low dram throughput and acceptable tensor activity, so the most plausible remaining headroom is fixed-shape control-path cleanup inside the existing two-stage pipeline.
- dir_02: Restore Linear PTX Export Order, Then Trim Export Scratch Sync And Lifetime | bottleneck: PTX export-path synchronization and shared scratch overhead in the active hot-band branch. The reversal experiment suggests traversal order matters, but it does not imply that the current linear export path is already minimal in sync count or scratch live range.
- dir_03: Keep GroupedRows 8 Fixed And Probe Within-Group Launch-Order Locality | bottleneck: CTA issue-order locality and L2 reuse rather than shared export or warp-local consume order. The active PTX kernel already has a grouped launch mapping; the open question is whether the order inside each fixed group is leaving cache locality on the table even with grouped_rows=8 held constant.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
