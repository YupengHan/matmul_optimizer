# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `deeb9765cb3ed49aa93e1d9cefc6b3beacd950f5`
- plateau counter: `1`
- round loop: `round 3/5`
- rounds remaining: `3`
- notes: `Node A completed round 2/5. Run node_b to continue round 3/5.`

## Latest measured custom run

- run id: `20260418_212022_bf16_gemm_v1_deeb976`
- run dir: `runs/20260418_212022_bf16_gemm_v1_deeb976`
- correctness: `FAIL`
- median runtime: `101.616016 ms`
- TFLOP/s: `7.154575 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

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
- current best custom gap: `75.457073 ms`, `3.911390x` slower than CUTLASS
