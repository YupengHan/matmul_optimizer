# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `bb3fc522e8e54b6da3644845bce77f2182f5f41c`
- plateau counter: `8`
- round loop: `round 1/20`
- rounds remaining: `20`
- notes: `Node C is ready to implement diagnosis_20260420_215833:dir_01 via recommended selection for round 1/20.`

## Latest measured custom run

- run id: `20260420_205720_bf16_gemm_v1_bb3fc52`
- run dir: `runs/20260420_205720_bf16_gemm_v1_bb3fc52`
- correctness: `PASS`
- median runtime: `25.381776 ms`
- TFLOP/s: `28.643363 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_215833`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/20 human-review audit: `state/human_review.md` still contributes only the approval gate and the exactly-one-direction rule, with no extra user-authored family to prioritize. The just-measured round spent its budget on an in-family retune of the active one-K 128x128 copy cadence, and node_a measured that branch slightly slower at 25.381776 ms than the 25.325055 ms accepted base. That is enough evidence to step away from the same immediate family for the next round. Accepted as the primary family for this diagnosis is the PTX one-K 128x128 control branch, because it preserves the current hot-band geometry and split while testing a different control/export path that already produced a nearby 25.379312 ms run. Deferred fallback families are the existing 256x128 pivot hot-band kernel and a light grouped-CTA traversal retune on the current 128x128 grid. Rejected for this round are reopening the two-K 128x128x32 stage-deepening path and the stale full-band 64x384 sweep-backed route.`
- dir_01: Reopen The PTX One-K 128x128 Hot-Band Control Branch | bottleneck: Hot-band inner-loop control and export overhead in the standard one-K 128x128 path, rather than the peeled 64x384 residual rows or the 64x96 tail.
- dir_02: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: CTA geometry and block-count overhead on the hot-band region, rather than a pure one-K copy-cadence problem.
- dir_03: Retune Hot-Band CTA Traversal On The 128x128 Grid | bottleneck: Inter-CTA locality and block traversal efficiency on the hot-band grid under register-limited low occupancy.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.495424 ms`, `0.942301x` slower than CUTLASS
