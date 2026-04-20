# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `fcc145b823a2c71c2a9055e6fb1d02ec2c51244e`
- plateau counter: `41`
- round loop: `round 16/17`
- rounds remaining: `2`
- notes: `Node C build succeeded for round 16/17. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_163839_bf16_gemm_v1_fcc145b`
- run dir: `runs/20260420_163839_bf16_gemm_v1_fcc145b`
- correctness: `PASS`
- median runtime: `26.043296 ms`
- TFLOP/s: `27.915799 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_163934`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 16/17 diagnosis for run 20260420_163839_bf16_gemm_v1_fcc145b. Human-review mapping for this round: keep the broad 64x384 control and non-PTX 128x128 control closed, and now also stop line-searching deeper into the seam family because 5888 regressed relative to the 6144 pivot. The fresh evidence is that the seam family has a local best already, while the accepted export base still has one meaningful untested prefetch variant left: the full A-before-B retime across both prime and refill. No new explicit human idea family is queued in state/human_review.md, so the ranking for the penultimate round is: accept the full prefetch retime first, keep the 4-row grouping as the best measured PTX fallback, and retain the 6144 seam only as the best measured launch-split fallback.`
- dir_01: Apply The Full PTX Prefetch Retime On The Accepted Export Base | bottleneck: Copy-pipeline handoff timing across both the initial stage prime and the future-tile refill in the PTX hot-band steady-state loop.
- dir_02: Keep The 4-Row PTX Grouping As The Best Measured PTX Fallback | bottleneck: Residual CTA grouping and orchestration overhead around the PTX hot-band grouped-row mapping.
- dir_03: Hold The 6144 Seam Variant As The Best Launch-Split Fallback | bottleneck: Boundary and launch split cost between the PTX hot-band kernel and the peeled 384-row row-band path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
