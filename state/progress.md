# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `0bd16bee053d0ce6cc862e8dfeef452d34c35bad`
- plateau counter: `22`
- round loop: `round 35/100`
- rounds remaining: `66`
- notes: `Node C build succeeded for round 35/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_074540_bf16_gemm_v1_0bd16be`
- run dir: `runs/20260421_074540_bf16_gemm_v1_0bd16be`
- correctness: `PASS`
- median runtime: `24.339969 ms`
- TFLOP/s: `29.869366 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_074640`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 35 is a textbook recovery diagnosis. The pair-scratch PTX export batching change from round 34 kept correctness and even shaved a little long-scoreboard stall, but it did not improve the machine state enough to win end-to-end; runtime regressed by 0.168961 ms and barrier stall ticked upward instead. That is enough evidence to close this exact sub-variant and recover to the accepted PTX base before exploring again.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Known register-limited plateau on the accepted PTX hot-band surface, used here as a recovery anchor after a measured loss.
- dir_02: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual PTX hot-band control-path overhead and live-range pressure on the restored one-K 128x128 surface, excluding the already-measured pair-scratch export sub-variant.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and synchronization strategy on the 256x128 hot-band path, plus correctness-sensitive writer ownership.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
