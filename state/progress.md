# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `af155a5bdaa475a7edba5ed1957b25a46454536e`
- plateau counter: `0`
- round loop: `single-run`
- rounds remaining: `0`
- notes: `Node A completed. Run node_b to produce exactly three directions from the latest measured summaries.`

## Latest measured custom run

- run id: `20260418_201228_bf16_gemm_v1_af155a5`
- run dir: `runs/20260418_201228_bf16_gemm_v1_af155a5`
- correctness: `PASS`
- median runtime: `145.344559 ms`
- TFLOP/s: `5.002041 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `pending_generation`
- diagnosis id: `None`
- recommended direction: `None`
- approved direction: `None`
- no directions recorded yet

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `119.426670 ms`, `5.607886x` slower than CUTLASS
