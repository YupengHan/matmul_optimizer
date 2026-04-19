# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `33e1461e09c0f90b0896452a94c16277f2a251db`
- plateau counter: `0`
- round loop: `round 18/20`
- rounds remaining: `3`
- notes: `Node C build succeeded for round 18/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_011243_bf16_gemm_v1_33e1461`
- run dir: `runs/20260419_011243_bf16_gemm_v1_33e1461`
- correctness: `PASS`
- median runtime: `41.534977 ms`
- TFLOP/s: `17.503788 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_011317`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- diagnosis notes: `Human-in-loop round: skip node_b diagnosis and run a fixed-shape tiling autotune sweep over 10+ candidate main widths, then preserve the results for later node_b use.`
- dir_01: Human idea: autotune fixed-shape main tiling across 10+ candidates | bottleneck: Search-space blindness rather than a single micro-bottleneck: we need real timing data for multiple tile widths to understand the trade between CTA count, DRAM pressure, MIO throttle, and register pressure.
- dir_02: Fallback: keep the current 64x192 main + 64x128 middle + 64x96 tail | bottleneck: No new hypothesis; this is a stability fallback while preserving the current best measured result.
- dir_03: Follow-up after sweep: promote a super-main width if the timing curve keeps improving | bottleneck: Potential remaining CTA-count overhead in the hot band if the timing curve continues improving as width grows.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `human_idea`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `15.617088 ms`, `1.602560x` slower than CUTLASS
