# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `22b4466b0ff3ca82c4a03efa03d07462cb5ca69c`
- plateau counter: `0`
- round loop: `round 47/100`
- rounds remaining: `54`
- notes: `Node A completed round 46/100. Run node_b to continue round 47/100.`

## Latest measured custom run

- run id: `20260420_073721_bf16_gemm_v1_22b4466`
- run dir: `runs/20260420_073721_bf16_gemm_v1_22b4466`
- correctness: `PASS`
- median runtime: `25.677312 ms`
- TFLOP/s: `28.313689 TFLOP/s`
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
- current best custom gap: `-0.240577 ms`, `0.990718x` slower than CUTLASS
