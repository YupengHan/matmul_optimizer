# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `8ba4496bd875ded3332c99af47abbc3b9c3d464b`
- plateau counter: `2`
- round loop: `round 6/20`
- rounds remaining: `15`
- notes: `Node A completed round 5/20. Run node_b to continue round 6/20.`

## Latest measured custom run

- run id: `20260420_222846_bf16_gemm_v1_8ba4496`
- run dir: `runs/20260420_222846_bf16_gemm_v1_8ba4496`
- correctness: `PASS`
- median runtime: `24.535040 ms`
- TFLOP/s: `29.631883 TFLOP/s`
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
- current best custom gap: `-1.740225 ms`, `0.932856x` slower than CUTLASS
