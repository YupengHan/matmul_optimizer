# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `6668d2193f6619c3de1cc6000711a62fc1f0fcd8`
- plateau counter: `95`
- round loop: `round 4/100`
- rounds remaining: `97`
- notes: `Node C is ready to implement diagnosis_20260421_114106:dir_01 via recommended selection for round 4/100.`

## Latest measured custom run

- run id: `20260421_113859_bf16_gemm_v1_6668d21`
- run dir: `runs/20260421_113859_bf16_gemm_v1_6668d21`
- correctness: `PASS`
- median runtime: `46.366718 ms`
- TFLOP/s: `15.679769 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_114106`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4/100 diagnosis emitted after a large measured regression on the PTX live-state trim.`
- dir_01: Restore the accepted PTX hot-band anchor after the failed live-state trim | bottleneck: Known register-limited plateau on the accepted 128x128 PTX surface; this direction is a recovery step, not a new bottleneck attack.
- dir_02: After recovery, retime the PTX barrier handoff without changing the shared footprint | bottleneck: synchronization_barrier_issue on the accepted PTX hot-band path
- dir_03: Keep the 256x128 half-panel repair alive, but only after the PTX base is recovered | bottleneck: occupancy_latency_hiding_issue on the wide geometry, with secondary barrier and short-scoreboard sensitivity

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
