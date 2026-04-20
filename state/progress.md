# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `046f075e6e6bba834990615cddaf89a3060fb4f1`
- plateau counter: `5`
- round loop: `round 44/100`
- rounds remaining: `57`
- notes: `Node A completed round 43/100. Run node_b to continue round 44/100.`

## Latest measured custom run

- run id: `20260420_021058_bf16_gemm_v1_046f075`
- run dir: `runs/20260420_021058_bf16_gemm_v1_046f075`
- correctness: `PASS`
- median runtime: `30.126080 ms`
- TFLOP/s: `24.132560 TFLOP/s`
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
- current best custom gap: `0.056383 ms`, `1.002175x` slower than CUTLASS
