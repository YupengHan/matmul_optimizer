# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `node_b_context_ready`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `9e20de18aa67dc6b5eb289d5e8e4c203dae37fa6`
- plateau counter: `0`
- round loop: `single-run`
- rounds remaining: `0`
- notes: `Fill state/latest_diagnosis.json with exactly three directions, then run node_b --finalize.`

## Latest measured custom run

- run id: `20260418_111959_bf16_gemm_v1_host_v0`
- run dir: `runs/20260418_111959_bf16_gemm_v1_host_v0`
- correctness: `PASS`
- median runtime: `802.842560 ms`
- TFLOP/s: `0.905557 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `awaiting_codex`
- diagnosis id: `diagnosis_20260418_174143`
- recommended direction: `None`
- approved direction: `None`
- dir_01: PENDING | bottleneck: PENDING
- dir_02: PENDING | bottleneck: PENDING
- dir_03: PENDING | bottleneck: PENDING

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `776.924671 ms`, `30.976387x` slower than CUTLASS
