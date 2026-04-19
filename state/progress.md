# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `c9d030a5022af8ce61bdcdb9b13e7ea85315ef52`
- plateau counter: `0`
- round loop: `round 5/5`
- rounds remaining: `1`
- notes: `Node A completed round 4/5. Run node_b to continue round 5/5.`

## Latest measured custom run

- run id: `20260419_140646_bf16_gemm_v1_c9d030a`
- run dir: `runs/20260419_140646_bf16_gemm_v1_c9d030a`
- correctness: `PASS`
- median runtime: `32.001088 ms`
- TFLOP/s: `22.718584 TFLOP/s`
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
- current best custom gap: `6.083199 ms`, `1.234710x` slower than CUTLASS
