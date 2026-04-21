# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `c2190a99f9933c10afbc772d325b1873689314a6`
- plateau counter: `28`
- round loop: `round 41/100`
- rounds remaining: `60`
- notes: `Node A completed round 40/100. Run node_b to continue round 41/100.`

## Latest measured custom run

- run id: `20260421_082405_bf16_gemm_v1_c2190a9`
- run dir: `runs/20260421_082405_bf16_gemm_v1_c2190a9`
- correctness: `PASS`
- median runtime: `24.180737 ms`
- TFLOP/s: `30.066058 TFLOP/s`
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
- notes: `No direction selected yet. Use approve, use-recommended-direction, or select-next after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
