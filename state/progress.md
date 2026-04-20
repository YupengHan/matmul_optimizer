# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `17a33b29fc2405c9fb3c5602d09a1c52bc42b32d`
- plateau counter: `0`
- round loop: `round 48/100`
- rounds remaining: `53`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 48/100.`

## Latest measured custom run

- run id: `20260420_074331_bf16_gemm_v1_17a33b2`
- run dir: `runs/20260420_074331_bf16_gemm_v1_17a33b2`
- correctness: `PASS`
- median runtime: `25.529328 ms`
- TFLOP/s: `28.477812 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_074354`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `- Round 47 separated the active PTX grouped-row policy from 4 and tuned it to 8, improving runtime from 25.677312 ms to 25.529328 ms and setting another best custom result, so block-order locality is still real.
- Coalescing Access: grouped-row=8 already reduced DRAM pressure sharply, so pure coalescing is no longer the lead diagnosis.
- Data Reuse: confirmed positive signal, because L2 throughput rose from 29.45% to 30.02% while DRAM dropped from 12.90% to 10.37%.
- Async Copy: cp.async is still doing useful work, but the current wait/commit cadence remains tied to full CTA sync points, so async-copy retuning is secondary rather than first priority.
- Bank Conflict: the current profile does not present a strong bank-conflict spike, so a layout-only rewrite is not the first move this round.
- L2 Cache: still worth refining via grouped-row/traversal experiments, but likely incremental now that the main locality win is already harvested.
- Register Reuse: now more important, because the PTX microkernel explicitly shortened A/B live ranges by reloading B per row-pair; that may be too conservative after the locality improvement.
- Pg2s: global-to-shared feed looks healthier than before, so it is no longer the clearest blocker.
- Ps2r: remains the best match for the elevated 4.77% mio_throttle, making B fragment reuse and shared-feed reduction the highest-priority direction.
- Stage: still worth keeping as a third option because barrier fell only to 7.18%, not to a negligible level.
- Priority comparison for this round: 1) go back to PTX B fragment / Ps2r / shared-feed first, 2) continue grouped-row size or traversal tuning only as a secondary locality refinement, 3) revisit stage cadence or another sync-oriented variant only after the feed path is retested.
- Ranking is set against the actual user goal of <20 ms, not just the narrower goal of staying ahead of the local CUTLASS baseline.`
- dir_01: Rebalance PTX B Fragment Reuse Against Ps2r Feed Pressure | bottleneck: Ps2r/shared-feed pressure in the PTX hot-band microkernel, showing up as elevated mio_throttle and underfed tensor issue despite lower DRAM demand.
- dir_02: Continue PTX Grouped-Row And Traversal Locality Tuning, But Treat It As Incremental | bottleneck: Residual block-order locality inefficiency in the PTX hot-band traversal, now mostly visible as an incremental L2/DRAM opportunity rather than the dominant limiter.
- dir_03: Revisit PTX Hot-Band Stage Cadence And Sync Granularity | bottleneck: Synchronization and stage-transition overhead in the PTX hot-band loop, with barrier cost still material even after the grouped-row locality win.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-0.388560 ms`, `0.985008x` slower than CUTLASS
