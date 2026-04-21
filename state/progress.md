# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `c643816563a8d5805f32896c9b0a041d34d27425`
- plateau counter: `1`
- round loop: `round 14/100`
- rounds remaining: `87`
- notes: `Node C build succeeded for round 14/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_000316_bf16_gemm_v1_c643816`
- run dir: `runs/20260421_000316_bf16_gemm_v1_c643816`
- correctness: `PASS`
- median runtime: `24.484832 ms`
- TFLOP/s: `29.692645 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_000409`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 14/100 audit: round 13 cleanly falsified the A-then-B PTX handoff retime on the correct PTX surface. The dominant kernel stayed `bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>`, but runtime regressed by 0.320559 ms and barrier rose from 5.43% to 6.29%. The current source differs from the round-12 best PTX surface by essentially one refill-order hunk, so the next action should be to restore that best surface first, then continue active-PTX exploration from a valid anchor while keeping the grouped_rows=8 round-history fallback alive.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Known-negative handoff ordering on the active PTX hot-band loop, where the A-then-B future refill increases effective barrier cost enough to overwhelm any scoreboard reduction.
- dir_02: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual PTX hot-band control-path overhead and consume-order friction on the restored one-K 128x128 PTX surface, beyond the already-closed A-then-B handoff variant.
- dir_03: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Consumer-side ordering and grouped-row locality inside the PTX hot-band microkernel under the grouped_rows=8 regime.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
