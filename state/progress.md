# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `310a8243e68c0bb6de2fed90d7d5074ab342567f`
- plateau counter: `100`
- round loop: `round 9/100`
- rounds remaining: `92`
- notes: `Node C is ready to implement diagnosis_20260421_123602:dir_01 via recommended selection for round 9/100.`

## Latest measured custom run

- run id: `20260421_123502_bf16_gemm_v1_310a824`
- run dir: `runs/20260421_123502_bf16_gemm_v1_310a824`
- correctness: `PASS`
- median runtime: `46.184448 ms`
- TFLOP/s: `15.741650 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_123602`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9/100 diagnosis emitted after the direct writer correctness fix erased the round-7 low-register gain, suggesting the next search unit should target a more compact full-row sweep rather than abandoning the signal immediately.`
- dir_01: Recover a compact correctness-safe 4-row PTX writer sweep | bottleneck: occupancy_latency_hiding_issue in the PTX export/store path if a compact full-row sweep can retain some of the low-register behavior while staying correct
- dir_02: Retime the barrier seam on the current correct 128x128 PTX anchor | bottleneck: synchronization_barrier_issue layered on top of occupancy_latency_hiding_issue in the current correctness-safe PTX anchor
- dir_03: Fallback to the current correctness-safe PTX writer anchor if compact sweeping stalls out | bottleneck: fallback recovery to the current correctness-safe PTX writer anchor

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
