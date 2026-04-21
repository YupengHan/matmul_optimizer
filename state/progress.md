# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `0893f2c709f4c3d8d592b75fb4df066f13a5bafa`
- plateau counter: `0`
- round loop: `round 2/20`
- rounds remaining: `19`
- notes: `Node C build succeeded for round 2/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_220130_bf16_gemm_v1_0893f2c`
- run dir: `runs/20260420_220130_bf16_gemm_v1_0893f2c`
- correctness: `PASS`
- median runtime: `24.419329 ms`
- TFLOP/s: `29.772294 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_220312`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2/20 human-review audit: the queue still contributes only the approval gate and the exactly-one-direction rule, with no extra user-authored family to prioritize. The just-finished round reopened the PTX one-k 128x128 control branch and turned it into the new accepted base at 24.419329 ms, which now beats the recorded CUTLASS baseline. Because that family already validated strongly, the best next use of the round budget is an orthogonal family test rather than another immediate local nibble on the same branch. Accepted as the primary family for this diagnosis is the existing 256x128 pivot hot-band kernel, because the hot-band wall is still 32.687232 ms with 200 registers per thread and only 16.62% active warps. Deferred fallback families are a bounded PTX-local exploit pass and a light traversal/locality retune on the current 128x128 PTX grid. Rejected again for this round are the standard one-k copy-cadence family, the two-K stage-deepening path, and the stale full-band 64x384 route.`
- dir_01: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Hot-band CTA geometry and block-count overhead on the current 128x128 PTX base, rather than a remaining local control-path bubble inside the winning branch.
- dir_02: Retune The Active PTX One-K 128x128 Hot-Band Control Path | bottleneck: Residual control-path overhead and live-range pressure inside the winning PTX one-k 128x128 hot-band branch.
- dir_03: Retune Hot-Band CTA Traversal On The 128x128 PTX Grid | bottleneck: Inter-CTA locality and traversal efficiency on the current 128x128 PTX hot-band grid.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.498560 ms`, `0.942180x` slower than CUTLASS
