# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `7e1004b94a18f7795b4a1f86bcc35c8b7e381250`
- plateau counter: `73`
- round loop: `round 86/100`
- rounds remaining: `15`
- notes: `Node A completed round 85/100. Run node_b to continue round 86/100.`

## Latest measured custom run

- run id: `20260421_084720_bf16_gemm_v1_7e1004b`
- run dir: `runs/20260421_084720_bf16_gemm_v1_7e1004b`
- correctness: `PASS`
- median runtime: `24.642097 ms`
- TFLOP/s: `29.503148 TFLOP/s`
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
