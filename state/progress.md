# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `97c626c4759a639f202e84018a585a5a854be08b`
- plateau counter: `29`
- round loop: `round 42/100`
- rounds remaining: `59`
- notes: `Node A completed round 41/100. Run node_b to continue round 42/100.`

## Latest measured custom run

- run id: `20260421_083825_bf16_gemm_v1_97c626c`
- run dir: `runs/20260421_083825_bf16_gemm_v1_97c626c`
- correctness: `PASS`
- median runtime: `24.535552 ms`
- TFLOP/s: `29.631264 TFLOP/s`
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
