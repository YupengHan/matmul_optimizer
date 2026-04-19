# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `4473555b78b0a2cfa211c4e9ca7c96dbd42353a8`
- plateau counter: `0`
- round loop: `round 5/5`
- rounds remaining: `1`
- notes: `Node A completed round 4/5. Run node_b to continue round 5/5.`

## Latest measured custom run

- run id: `20260418_213511_bf16_gemm_v1_4473555`
- run dir: `runs/20260418_213511_bf16_gemm_v1_4473555`
- correctness: `PASS`
- median runtime: `88.543102 ms`
- TFLOP/s: `8.210910 TFLOP/s`
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
- current best custom gap: `62.625214 ms`, `3.416293x` slower than CUTLASS
