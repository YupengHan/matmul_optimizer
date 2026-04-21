# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `51bdc044b098b1d42bd99cf1cf88e8d019d406f1`
- plateau counter: `69`
- round loop: `round 82/100`
- rounds remaining: `19`
- notes: `Node A completed round 81/100. Run node_b to continue round 82/100.`

## Latest measured custom run

- run id: `20260421_084643_bf16_gemm_v1_51bdc04`
- run dir: `runs/20260421_084643_bf16_gemm_v1_51bdc04`
- correctness: `PASS`
- median runtime: `24.943105 ms`
- TFLOP/s: `29.147110 TFLOP/s`
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
