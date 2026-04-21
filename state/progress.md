# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `ab3bbb20c3decc5c173a0fbada0eba99b61bfff5`
- plateau counter: `11`
- round loop: `round 24/100`
- rounds remaining: `77`
- notes: `Node C is ready to implement diagnosis_20260421_010129:dir_01 via recommended selection for round 24/100.`

## Latest measured custom run

- run id: `20260421_010044_bf16_gemm_v1_ab3bbb2`
- run dir: `runs/20260421_010044_bf16_gemm_v1_ab3bbb2`
- correctness: `FAIL`
- median runtime: `30.081952 ms`
- TFLOP/s: `24.167960 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_010129`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 24 closes the immediate half-panel continuation: the branch preserved the occupancy breakthrough but failed correctness twice in a row and did not recover runtime. The next best move is to restore a correct baseline first, then choose the next aggressive family from there.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: No new bottleneck is being attacked here; this is an exact recovery of the best-known implementation surface.
- dir_02: Restore The Grouped-Row Non-PTX 128x128 Sibling Surface | bottleneck: This is a safe alternate-surface recovery, not a new bottleneck attack.
- dir_03: Retune The Auxiliary 256x128 Hot-Band K-Loop Schedule | bottleneck: Hot-band K-loop scheduling and latency hiding on a broader 256x128 reuse regime rather than the plateaued 128x128 surfaces.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
