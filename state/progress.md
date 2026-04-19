# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `2a86c71387e520f89bd133d824161d17428f4242`
- plateau counter: `1`
- round loop: `round 7/20`
- rounds remaining: `14`
- notes: `Node C build succeeded for round 7/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260418_230727_bf16_gemm_v1_2a86c71`
- run dir: `runs/20260418_230727_bf16_gemm_v1_2a86c71`
- correctness: `PASS`
- median runtime: `57.120176 ms`
- TFLOP/s: `12.727892 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_231124`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Restore the low-footprint wide B slab and keep any new swizzle occupancy-neutral | bottleneck: Shared-memory footprint and B-fragment load efficiency are cutting block residency and leaving the tensor loop underfed.
- dir_02: Retune the CTA and per-warp N tile so B-side experiments do not burn residency | bottleneck: Occupancy and latency hiding are constrained by the current CTA tile shape and its shared-memory budget.
- dir_03: Specialize the fixed-shape mainloop so the async pipeline pays less per-step control and sync overhead | bottleneck: Synchronization and fixed-shape control overhead in the steady-state async-copy and MMA loop.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `28.219023 ms`, `2.088786x` slower than CUTLASS
