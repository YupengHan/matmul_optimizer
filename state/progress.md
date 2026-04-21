# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `f768e80d950fa4cd036ea003b32af972278df540`
- plateau counter: `94`
- round loop: `round 3/100`
- rounds remaining: `98`
- notes: `Node C is ready to implement diagnosis_20260421_113657:dir_01 via recommended selection for round 3/100.`

## Latest measured custom run

- run id: `20260421_111322_bf16_gemm_v1_f768e80`
- run dir: `runs/20260421_111322_bf16_gemm_v1_f768e80`
- correctness: `PASS`
- median runtime: `24.293376 ms`
- TFLOP/s: `29.926653 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_113657`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3/100 diagnosis re-emitted after clearing the partial node_c edit and rerunning node_b.`
- dir_01: Trim live state inside the recovered 128x128 PTX hot-band control path | bottleneck: occupancy_latency_hiding_issue with a secondary tensor_core_underutilization component on the accepted 128x128 PTX hot-band path
- dir_02: Collapse PTX wait-group and consumer barrier cadence without growing shared state | bottleneck: synchronization_barrier_issue with occupancy_latency_hiding_issue as the guardrail
- dir_03: Repair the 256x128 half-panel register-reuse branch with compact B staging | bottleneck: occupancy_latency_hiding_issue on the wide hot-band geometry, with secondary synchronization_barrier_issue and short_scoreboard sensitivity

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
