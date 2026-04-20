# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `8ed8cf3986c9133763b44419329dced785f78152`
- plateau counter: `32`
- round loop: `round 7/17`
- rounds remaining: `11`
- notes: `Node C build succeeded for round 7/17. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_160231_bf16_gemm_v1_8ed8cf3`
- run dir: `runs/20260420_160231_bf16_gemm_v1_8ed8cf3`
- correctness: `PASS`
- median runtime: `25.771520 ms`
- TFLOP/s: `28.210188 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_160310`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 7/17 diagnosis for run 20260420_160231_bf16_gemm_v1_8ed8cf3. Human-review mapping for this round: keep broad retile/default-promotion reopening low priority, and keep the immediate prefetch-handoff, expanded B-shared-skew, and grouped-row-window families closed. Round 5 proved the multi-gap B-shared layout was invalid because correctness failed 3/3, and round 6 proved the grouped-row retune stayed correct but still regressed to 25.77151966 ms with long-scoreboard rising to 7.83 and DRAM nudging up to 11.74. No new explicit human idea family is queued in state/human_review.md, so the surviving ranking is: accept one last minimal PTX export-address cleanup as the primary narrow move on top of the accepted base 20260420_154827_bf16_gemm_v1_7adfc4e at 25.50532818 ms; defer the historically measured 64x384 fixed-main-tile control because its evidence is older and broader; keep the non-PTX 128x128 sibling only as a fallback control.`
- dir_01: Apply Only A Minimal PTX Export Address Cleanup | bottleneck: Residual address-generation and store-helper overhead in the surviving PTX export path.
- dir_02: Reopen The Measured 64x384 Fixed-Main-Tile Control Path | bottleneck: Broader hot-band path selection and arithmetic-intensity tradeoff rather than PTX microkernel control overhead.
- dir_03: Use The Non-PTX 128x128 Sibling As A Control | bottleneck: PTX-specific export/store complexity versus the simpler non-PTX 128x128 sibling.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
