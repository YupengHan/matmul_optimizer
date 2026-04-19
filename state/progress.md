# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `eecbb72cf2ce923b80d7eab679b5355a3873fc88`
- plateau counter: `0`
- round loop: `round 2/20`
- rounds remaining: `19`
- notes: `Node A completed round 1/20. Run node_b to continue round 2/20.`

## Latest measured custom run

- run id: `20260418_221951_bf16_gemm_v1_eecbb72`
- run dir: `runs/20260418_221951_bf16_gemm_v1_eecbb72`
- correctness: `PASS`
- median runtime: `82.266624 ms`
- TFLOP/s: `8.837356 TFLOP/s`
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
- current best custom gap: `56.348736 ms`, `3.174125x` slower than CUTLASS
