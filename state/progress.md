# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `17a33b29fc2405c9fb3c5602d09a1c52bc42b32d`
- plateau counter: `0`
- round loop: `round 48/100`
- rounds remaining: `53`
- notes: `Node A completed round 47/100. Run node_b to continue round 48/100.`

## Latest measured custom run

- run id: `20260420_074331_bf16_gemm_v1_17a33b2`
- run dir: `runs/20260420_074331_bf16_gemm_v1_17a33b2`
- correctness: `PASS`
- median runtime: `25.529328 ms`
- TFLOP/s: `28.477812 TFLOP/s`
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
- current best custom gap: `-0.388560 ms`, `0.985008x` slower than CUTLASS
