# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `0c534cb56c1dcf9b48171528ba70bb2028aef44e`
- plateau counter: `10`
- round loop: `round 23/100`
- rounds remaining: `78`
- notes: `Node C is ready to implement diagnosis_20260421_005735:dir_01 via recommended selection for round 23/100.`

## Latest measured custom run

- run id: `20260421_005653_bf16_gemm_v1_0c534cb`
- run dir: `runs/20260421_005653_bf16_gemm_v1_0c534cb`
- correctness: `FAIL`
- median runtime: `29.819424 ms`
- TFLOP/s: `24.380734 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_005735`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 23 interprets the half-panel result as partial signal, not a total miss. The branch remained wrong and too slow, but it reproduced the historical occupancy breakthrough on the current environment. That justifies one final targeted continuation before mechanically restoring to a plateau surface.`
- dir_01: Single-Source Warp Ownership End To End On The Half-Panel Branch | bottleneck: Half-panel ownership and export correctness on top of a branch that already solved the live-state wall but still pays excessive synchronization.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: No new bottleneck is being attacked; this is an exact recovery of the best-known implementation surface.
- dir_03: Restore The Grouped-Row Non-PTX 128x128 Sibling Surface | bottleneck: This is a safe alternate-surface recovery, not a new bottleneck attack.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
