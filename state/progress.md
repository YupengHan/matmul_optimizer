# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `d8e9048d7887e2c2e735dde93e5e75165800b3cd`
- plateau counter: `34`
- round loop: `round 9/17`
- rounds remaining: `9`
- notes: `Node C build succeeded for round 9/17. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_160736_bf16_gemm_v1_d8e9048`
- run dir: `runs/20260420_160736_bf16_gemm_v1_d8e9048`
- correctness: `PASS`
- median runtime: `25.959904 ms`
- TFLOP/s: `28.005474 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_160829`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9/17 diagnosis for run 20260420_160736_bf16_gemm_v1_d8e9048. Human-review mapping for this round: keep the deeper export cleanup from round 8 closed, and continue to keep the expanded B-shared-skew and grouped-row-window families closed after their measured losses. The key new evidence is that round 7 established a new accepted base at 24.84582424 ms with the minimal export-address cleanup, while round 8 showed that pushing the row-pair export cleanup further regressed sharply to 25.95990372. That means the export family is no longer the best immediate lever beyond the accepted base. No new explicit human idea family is queued in state/human_review.md, so the ranking now shifts to: accept a narrower PTX prefetch-handoff retime on top of the new accepted export base, defer the older-but-measured 64x384 control as the main broader fallback, and keep the non-PTX 128x128 sibling as a tertiary control path.`
- dir_01: Reopen PTX Prefetch Handoff On Top Of The New Export Base | bottleneck: Copy-pipeline handoff timing and future-tile refill cadence in the PTX hot-band steady-state loop.
- dir_02: Reopen The Measured 64x384 Fixed-Main-Tile Control Path | bottleneck: Broader hot-band path selection and arithmetic-intensity tradeoff rather than PTX helper overhead.
- dir_03: Use The Non-PTX 128x128 Sibling As A Control | bottleneck: PTX-specific export/store and prefetch orchestration versus the simpler non-PTX 128x128 sibling.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
