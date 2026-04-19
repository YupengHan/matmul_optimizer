# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `3265675318dd0108296bfc9c83879cc130bb6351`
- plateau counter: `0`
- round loop: `round 5/20`
- rounds remaining: `16`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 5/20.`

## Latest measured custom run

- run id: `20260418_225011_bf16_gemm_v1_3265675`
- run dir: `runs/20260418_225011_bf16_gemm_v1_3265675`
- correctness: `PASS`
- median runtime: `63.126495 ms`
- TFLOP/s: `11.516867 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_225054`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Retile to a 4-warp CTA so each K-slice carries more MMA work and more resident warps | bottleneck: Occupancy ceiling and synchronization-limited tensor-core utilization in the steady-state mainloop
- dir_02: Replace the simple B-row skew with a stronger shared-memory swizzle for WMMA loads | bottleneck: Shared-memory/L1 bank and MIO pressure on B fragment loads
- dir_03: Remove the shared scratch epilogue and emit BF16 stores from registers with wider vectors | bottleneck: Epilogue LSU/MIO pressure from shared scratch traffic and scalar BF16 stores

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `37.208607 ms`, `2.435634x` slower than CUTLASS
