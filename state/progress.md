# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `awaiting_direction_selection_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `8dcab81ea44e6d66b1f22c2a768c8e9d3b21223f`
- plateau counter: `92`
- round loop: `single-run`
- rounds remaining: `0`
- notes: `Node B completed. Approve a direction or explicitly use the recommended direction before node_c.`

## Latest measured custom run

- run id: `20260421_105134_bf16_gemm_v1_8dcab81`
- run dir: `runs/20260421_105134_bf16_gemm_v1_8dcab81`
- correctness: `PASS`
- median runtime: `24.186960 ms`
- TFLOP/s: `30.058321 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_105526`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Re-evaluated the active live queue using the richer NCU diagnosis handoff; promoted register- and barrier-aligned families and demoted export-only families.`
- dir_01: Transplant low-register half-panel staging into the correctness-safe 256x128 pivot | bottleneck: occupancy_latency_hiding_issue with tensor_core_underutilization driven by register pressure and oversized live state
- dir_02: Trim live state inside the active 128x128 PTX control path before more epilogue work | bottleneck: occupancy_latency_hiding_issue on the accepted PTX hot-band path, with a smaller synchronization_barrier_issue component
- dir_03: Collapse PTX wait-group and sync cadence without growing the shared-memory footprint | bottleneck: synchronization_barrier_issue with smaller occupancy side-effects on the PTX 128x128 microkernel

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve, use-recommended-direction, or select-next after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
