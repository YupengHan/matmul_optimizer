# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `3713ac4a81a442594f565309bb52b84291b0e391`
- plateau counter: `4`
- round loop: `round 52/100`
- rounds remaining: `49`
- notes: `Node A completed round 51/100. Run node_b to continue round 52/100.`

## Latest measured custom run

- run id: `20260420_081140_bf16_gemm_v1_3713ac4`
- run dir: `runs/20260420_081140_bf16_gemm_v1_3713ac4`
- correctness: `PASS`
- median runtime: `25.716736 ms`
- TFLOP/s: `28.270284 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

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
