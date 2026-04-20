# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `96154e330bd119b7572aeb4ff4722232a73b2a80`
- plateau counter: `6`
- round loop: `round 65/100`
- rounds remaining: `36`
- notes: `Node C build succeeded for round 65/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_091644_bf16_gemm_v1_96154e3`
- run dir: `runs/20260420_091644_bf16_gemm_v1_96154e3`
- correctness: `PASS`
- median runtime: `25.560576 ms`
- TFLOP/s: `28.442998 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_091814`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 65/100 diagnosis is anchored to run 20260420_091644_bf16_gemm_v1_96154e3 at 25.56057644 ms, but the optimization target remains under 20 ms. The accepted best custom kernel is still round 58 at 24.57088089 ms on commit 4e5579ec72e9b1f05820c895c0315235d66f30cd, so the round-64 source is explicitly treated as a regression family rather than a new base because it changed kFixedHotBandPtxGroupedRows from the accepted 8 to 6. Audit against the human idea families: tiling is already accepted only as the current 64x64 warp microtile, while any broader 256x128 macro-tiling reopen is rejected for this round; coalescing / wide global access is already accepted in the 16-byte cp.async path; shared-memory reuse is already accepted in the staged A/B tiles; async copy is already accepted; bank-conflict handling is accepted only through the current right-left PTX 64x64 consume order plus the existing padded export scratch, while the row-pair-dependent split sweep and the fully mirrored sweep are closed negatives; L2 cache / launch-order locality is accepted only as grouped_rows=8, while grouped_rows=16, grouped_rows=4, and grouped_rows=6 are all rejected for this round; register reuse Right-Left-Right-Left is already accepted in the base and should not be reopened as a new broad family; Pg2s double buffer is already accepted in the base; Ps2r double buffer is rejected for this round because extra-live B lookahead, K32 cadence, and warmup-order reopen are already closed; stage/multi-buffer is accepted only in the current one-sync steady-state handoff with B-first refill and unroll 2, while A-first refill, unroll 1, CTA-level B repack, and broader pipeline rewrites are rejected. The measured evidence supports that ranking: round 64 keeps the same hot-kernel occupancy/resource shape as round 58, but loses time while DRAM rises from 9.75 to 11.58, barrier rises from 5.04 to 5.35, and long scoreboard rises from 7.31 to 7.69, so the next best single node_c is not another feed-path or grouped_rows rewrite. Dir_01 is recommended because it first restores the accepted grouped_rows=8 base and then makes the smallest auditable new change still attached to that accepted PTX hot-band branch: align PTX export/live-range order with the reversed compute row-pair traversal. Dir_02 keeps the accepted stage family open but is riskier because handoff retiming can easily drift into already closed refill branches. Dir_03 is the remaining locality family, but only as a fixed-group-size closure and not as another grouped_rows sweep.`
- dir_01: Restore grouped_rows=8, then align PTX export order with the reversed compute row-pair traversal | bottleneck: PTX hot-band export/writeback ordering and accumulator live-range mismatch after the accepted grouped_rows=8 locality base is restored.
- dir_02: Restore grouped_rows=8, then retime the accepted one-sync B-first handoff without reopening closed refill branches | bottleneck: Residual producer-consumer overlap loss in the accepted one-sync steady-state handoff rather than consumer order or global-memory vectorization.
- dir_03: Restore grouped_rows=8, then try an intra-group launch-order closure without changing the group size | bottleneck: Residual hot-band L2 / launch-order locality loss inside the accepted grouped_rows=8 dispatch path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
