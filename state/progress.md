# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `63d2fafdf1de4fcbc09b734f8f6f3a3320e8b1b7`
- plateau counter: `15`
- round loop: `round 10/10`
- rounds remaining: `1`
- notes: `Node A completed round 9/10. Run node_b to continue round 10/10.`

## Latest measured custom run

- run id: `20260419_214140_bf16_gemm_v1_63d2faf`
- run dir: `runs/20260419_214140_bf16_gemm_v1_63d2faf`
- correctness: `PASS`
- median runtime: `30.856704 ms`
- TFLOP/s: `23.561150 TFLOP/s`
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
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
