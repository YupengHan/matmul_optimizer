# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `0893f2c709f4c3d8d592b75fb4df066f13a5bafa`
- plateau counter: `0`
- round loop: `round 2/20`
- rounds remaining: `19`
- notes: `Node A completed round 1/20. Run node_b to continue round 2/20.`

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

- diagnosis status: `pending_generation`
- diagnosis id: `None`
- recommended direction: `None`
- approved direction: `None`
- diagnosis notes: `Run node_b to produce exactly three directions from the latest measured run.`
- no directions recorded yet

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve, use-recommended-direction, or select-next after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.498560 ms`, `0.942180x` slower than CUTLASS
