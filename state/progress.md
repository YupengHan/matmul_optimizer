# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `134df2982fe154e85e9b0d1b62207275ee201a27`
- plateau counter: `2`
- round loop: `round 13/20`
- rounds remaining: `8`
- notes: `Node C build succeeded for round 13/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_002116_bf16_gemm_v1_134df29`
- run dir: `runs/20260419_002116_bf16_gemm_v1_134df29`
- correctness: `PASS`
- median runtime: `46.005760 ms`
- TFLOP/s: `15.802791 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_002159`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `This diagnosis incorporates aggressive exploration and human-in-loop guidance.`
- dir_01: Rewrite shared fragment delivery to cut MIO pressure | bottleneck: Shared-memory fragment delivery and MIO saturation from the current CTA-wide staging plus warp-group B skew, not CTA barrier cadence.
- dir_02: Collapse the epilogue scratch and scalar writeback path | bottleneck: Epilogue/writeback overhead from shared scratch plus scalar output stores diluting tensor-core work.
- dir_03: Retile warp ownership to raise tensor density and active warps | bottleneck: Poor CUDA-core vs tensor-core work partitioning from the present CTA/warp tile shape, not synchronization frequency.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `17.779776 ms`, `1.686004x` slower than CUTLASS
