# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `ea27d5a906ceb46b0a4ec429d6d53f4a457620d6`
- plateau counter: `0`
- round loop: `round 19/20`
- rounds remaining: `2`
- notes: `Node A completed round 18/20. Run node_b to continue round 19/20.`

## Latest measured custom run

- run id: `20260419_013130_bf16_gemm_v1_ea27d5a`
- run dir: `runs/20260419_013130_bf16_gemm_v1_ea27d5a`
- correctness: `PASS`
- median runtime: `38.473728 ms`
- TFLOP/s: `18.896516 TFLOP/s`
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
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `12.555840 ms`, `1.484447x` slower than CUTLASS
