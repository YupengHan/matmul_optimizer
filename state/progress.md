# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `c26ac4fdc00ad89cefc324b30d4fc8758fb4d0af`
- plateau counter: `0`
- round loop: `round 28/50`
- rounds remaining: `23`
- notes: `Node A completed round 27/50. Run node_b to continue round 28/50.`

## Latest measured custom run

- run id: `20260420_002119_bf16_gemm_v1_c26ac4f`
- run dir: `runs/20260420_002119_bf16_gemm_v1_c26ac4f`
- correctness: `PASS`
- median runtime: `27.022336 ms`
- TFLOP/s: `26.904388 TFLOP/s`
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
- current best custom gap: `1.104447 ms`, `1.042613x` slower than CUTLASS
