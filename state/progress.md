# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `273d63c0dca706eb94e279d165295463933a4b5c`
- plateau counter: `0`
- round loop: `round 22/50`
- rounds remaining: `29`
- notes: `Node A completed round 21/50. Run node_b to continue round 22/50.`

## Latest measured custom run

- run id: `20260420_001122_bf16_gemm_v1_273d63c`
- run dir: `runs/20260420_001122_bf16_gemm_v1_273d63c`
- correctness: `PASS`
- median runtime: `28.949504 ms`
- TFLOP/s: `25.113364 TFLOP/s`
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
- current best custom gap: `3.031615 ms`, `1.116970x` slower than CUTLASS
