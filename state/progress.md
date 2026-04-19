# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `2872f92585773d6f6a38c911cb76d010d4209366`
- plateau counter: `0`
- round loop: `round 2/5`
- rounds remaining: `4`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 2/5.`

## Latest measured custom run

- run id: `20260419_102608_bf16_gemm_v1_2872f92`
- run dir: `runs/20260419_102608_bf16_gemm_v1_2872f92`
- correctness: `PASS`
- median runtime: `35.677088 ms`
- TFLOP/s: `20.377768 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_102638`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2/5 diagnosis prepared from the current best custom run 20260419_102608_bf16_gemm_v1_2872f92 at 35.677088 ms. Recent history is applied explicitly: broad B-feed rewrites and phased live-set rewrites regressed, peeled hot-kernel specialization plus trimmed export won, and deeper single-skew overlap improved again. Ranking therefore keeps the peeled 64x384 hot kernel as the base, prioritizes barrier/stage-recycle cleanup next, then further export trimming, and leaves tail specialization as the lower-upside third option.`
- dir_01: Reduce stage-recycle barriers in the peeled 64x384 hot loop | bottleneck: CTA-wide synchronization and stage handoff overhead inside the peeled 64x384 steady-state loop.
- dir_02: Trim the peeled hot-kernel export path beyond the current quad writeback | bottleneck: Epilogue-side shared export and LSU pressure after the peeled hot loop finishes MMA.
- dir_03: Peel and specialize the fixed 64x96 tail kernel to match the hot path | bottleneck: Residual tail overhead from using the generic 64x96 tensor-core kernel on a fixed-shape tail region.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `9.759199 ms`, `1.376543x` slower than CUTLASS
