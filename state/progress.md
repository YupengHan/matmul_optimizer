# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `e6fdb8b21ac8bff36d581073faf117875347f3ea`
- plateau counter: `7`
- round loop: `round 16/50`
- rounds remaining: `35`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 16/50.`

## Latest measured custom run

- run id: `20260420_200110_bf16_gemm_v1_e6fdb8b`
- run dir: `runs/20260420_200110_bf16_gemm_v1_e6fdb8b`
- correctness: `PASS`
- median runtime: `25.325055 ms`
- TFLOP/s: `28.707516 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_200135`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 16/50 human-review audit: `state/human_review.md` still contributes only the approval/selection gate and the exactly-one-direction rule, with no extra user-authored idea family to prioritize. Accepted as the primary family for this round: bounded in-family tuning on the active one-K `128x128` hot-band path, because the current kernel source already matches the recorded best-custom `1181247` source in `src/kernels/bf16_gemm_v1.cu`, and the latest NCU evidence says only the dominant hot-band kernel is slightly behind that best reference (`32,917,184 ns` now versus `32,868,864 ns` on `1181247`, with `7.73%` versus `7.49%` long-scoreboard and `13.02%` versus `12.84%` DRAM). Deferred fallback families: the PTX one-K `128x128` control branch and the existing `256x128` pivot hot-band branch, both kept as single-direction A/B paths that still satisfy the human-review gate. Rejected as the primary family for this round: reopening the two-K `128x128x32` stage-deepening path, because the latest recovery came directly from removing it; also rejected again as a primary move is the stale sweep-backed full-band `64x384` family from `state/autotune_round18_main_tiles.md`, because direct node_a evidence on the restored surface already showed that reopening it regressed badly to `34.016768 ms`.`
- dir_01: Retune The Active One-K 128x128 Hot-Band Copy Cadence | bottleneck: A narrow hot-band feed-latency and shared-stage handoff gap inside the active one-K `128x128` kernel, not the peeled `64x384` residual rows or the `64x96` tail.
- dir_02: Reopen The PTX One-K 128x128 Hot-Band Control Branch | bottleneck: Hot-band inner-loop control and accumulate/export behavior in the standard one-K `128x128` branch, addressed by the PTX control path rather than by changing CTA geometry.
- dir_03: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Hot-band CTA geometry and block-count overhead in the current four-warp `128x128` path, rather than a pure copy-cadence issue.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.495424 ms`, `0.942301x` slower than CUTLASS
