# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `10d32cf805efc73140de4de50b5aa8a57abda726`
- plateau counter: `30`
- round loop: `round 5/17`
- rounds remaining: `13`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 5/17.`

## Latest measured custom run

- run id: `20260420_155247_bf16_gemm_v1_10d32cf`
- run dir: `runs/20260420_155247_bf16_gemm_v1_10d32cf`
- correctness: `PASS`
- median runtime: `25.982464 ms`
- TFLOP/s: `27.981158 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_155518`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5/17 diagnosis for run 20260420_155247_bf16_gemm_v1_10d32cf. Human-review mapping for this round: reject broad retile/default-promotion reopening and reject the immediate PTX prefetch-handoff family for now, because round 4 cut long-scoreboard to 5.83 but still regressed by +0.47713566 ms versus the accepted base, with barrier rising to 6.63 and no throughput gain. Also keep deeper export flattening closed after round 3. No new explicit human idea family is queued in state/human_review.md, so this round carries forward the surviving narrow idea families only: accept PTX B-shared skew as the primary next move, defer grouped-row/orchestration retuning as the main alternate, and keep only a minimal export cleanup as the low-risk reserve. The older main-tile sweep data is noted but not reopened this round because tonight's loop is staying on the accepted PTX baseline rather than broad branch changes.`
- dir_01: Tune PTX Hot-Band B-Shared Skew On The Accepted Export Base | bottleneck: Shared-memory B-fragment layout friction and address-generation overhead in the PTX hot-band path.
- dir_02: Retighten PTX Hot-Band Grouping / Orchestration Window | bottleneck: Hot-band CTA grouping and orchestration overhead around the PTX grouped-row mapping.
- dir_03: Apply Only A Minimal PTX Export Address Cleanup | bottleneck: Residual address-generation and store-helper overhead in the surviving PTX export path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
