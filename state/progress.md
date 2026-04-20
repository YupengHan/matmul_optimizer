# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `885b82bed9101254e2b9622f7ed493a9ffff7501`
- plateau counter: `10`
- round loop: `round 69/100`
- rounds remaining: `32`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 69/100.`

## Latest measured custom run

- run id: `20260420_095109_bf16_gemm_v1_885b82b`
- run dir: `runs/20260420_095109_bf16_gemm_v1_885b82b`
- correctness: `PASS`
- median runtime: `25.857952 ms`
- TFLOP/s: `28.115893 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_104405`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 69 diagnosis is anchored to run 20260420_095109_bf16_gemm_v1_885b82b at 25.85795212 ms. The target remains below 20 ms, and the accepted best custom result is still round 58 at 24.57088089 ms on commit 4e5579ec72e9b1f05820c895c0315235d66f30cd. Round 68 closed the grouped_rows=8 snake launch-order mapping as a negative because runtime regressed, even though the measured metrics on that run were tensor 48.22, dram 10.38, lts 31.24, barrier 6.48, long_scoreboard 4.12, and mio 3.31. That stall mix is exactly why implementation-surface drift is the main concern for this round: the current source may not actually equal the accepted round-58 implementation surface plus only the intended later narrow closures. The supervisor already found surviving deltas beyond the just-failed snake mapping: the missing second syncwarp in ptx_wmma_store_tile_row_pairs_64x64_ptx_microkernel, the changed B-before-A stage order in advance_peeled_hot_stage_ptx, the changed unroll in bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel from 1 to 2, the extra RowPairBase template parameter in ptx_wmma_load_col_fragment_64x64_ptx_microkernel, and the current snake mapping itself. Human-idea audit: tiling is already accepted only as the existing hot-band tile hierarchy, so a new tiling reopen is deferred; coalescing and wide global access are already accepted through the current async-copy path; shared-memory reuse is already accepted; async copy is already accepted; bank-conflict handling is accepted only through the current right-left consume order and should not reopen consumer-order sweeps; L2 locality is now closed for snake mapping and for grouped_rows sweeps, so locality is not the next family; register reuse is already accepted in the current right-left consume order and should not reopen sweep variants; Pg2s is already accepted; Ps2r remains closed through the previously rejected extra-live, K32 cadence, and warmup-order families; stage work is accepted only as the narrow one-sync, B-first base, while fixed-K peeling is already closed-negative. Ranking rationale: dir_01 is the best next move because it removes the baseline ambiguity and restores an auditable foundation for every later micro-optimization. Dir_02 is the remaining still-open narrow stage-family move once the exact base is back. Dir_03 stays available only as a low-priority export-lifetime cleanup, explicitly treating round 67 as evidence that export-side second-sync removal is not a primary runtime lever.`
- dir_01: Restore the exact accepted round-58 implementation surface first, then re-measure from that true base | bottleneck: Baseline drift and false-anchor risk rather than a single hot-path micro-bottleneck; the loop needs the true accepted surface back before further diagnosis is trustworthy.
- dir_02: After exact-base restore, test only a very narrow one-sync handoff closure on the active PTX hot-band loop | bottleneck: Residual one-sync consumer-to-refill overlap loss on the true accepted PTX hot-band base.
- dir_03: After exact-base restore, probe a low-priority export-side lifetime closure that keeps linear export order | bottleneck: Residual export writeback and scratch-lifetime overhead on the exact accepted base, after accepting that second-sync removal alone is not a primary runtime lever.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
