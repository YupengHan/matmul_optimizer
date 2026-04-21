# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `paused_on_explicit_user_redirect`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `fc400df814258c9927aa72a78b213b2e9325787f`
- plateau counter: `102`
- round loop: `single-run`
- rounds remaining: `90`
- notes: `Paused on explicit user redirect after round 10/100. Resume from node_b for round 11/100 by filling state/latest_diagnosis.json for run 20260421_124420_bf16_gemm_v1_fc400df, then run node_b --finalize.`

## Latest measured custom run

- run id: `20260421_124420_bf16_gemm_v1_fc400df`
- run dir: `runs/20260421_124420_bf16_gemm_v1_fc400df`
- correctness: `PASS`
- median runtime: `45.920258 ms`
- TFLOP/s: `15.832216 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `awaiting_codex`
- diagnosis id: `diagnosis_20260421_125336`
- recommended direction: `None`
- approved direction: `None`
- diagnosis notes: `Paused on explicit user redirect after node_b context prep. Resume by filling exactly three directions for run 20260421_124420_bf16_gemm_v1_fc400df, then run node_b --finalize. Frontier was led by diagnosis_20260421_013125:dir_02 (restore exact 489574e surface), while the low-register writer family remains strategically important.`
- dir_01: PENDING | bottleneck: PENDING
- dir_02: PENDING | bottleneck: PENDING
- dir_03: PENDING | bottleneck: PENDING

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve, use-recommended-direction, or select-next after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
