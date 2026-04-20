# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `f71a41fdee677a3f78b9124bae317e3e96ba4983`
- plateau counter: `1`
- round loop: `round 60/100`
- rounds remaining: `41`
- notes: `Node C build succeeded for round 60/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_085640_bf16_gemm_v1_f71a41f`
- run dir: `runs/20260420_085640_bf16_gemm_v1_f71a41f`
- correctness: `PASS`
- median runtime: `25.995744 ms`
- TFLOP/s: `27.966864 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_085737`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Anchored to latest measured run 20260420_085640_bf16_gemm_v1_f71a41f at 25.995744 ms. Use the accepted grouped_rows=8 + reversed row-pair traversal + one-sync handoff base as the starting point and keep rejected branches closed.`
- dir_01: Restore accepted base, then test mirrored hot-band column sweep | bottleneck: Bad instruction-flow and locality interaction from the failed row-pair-dependent column split, rather than the accepted base traversal itself.
- dir_02: Recover overlap behind the one-sync handoff | bottleneck: Residual latency in the handoff window between row-pair traversal and the next shared-memory/compute phase.
- dir_03: Small locality closure only | bottleneck: Minor cache/shared-memory locality losses rather than a structural scheduling problem.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
