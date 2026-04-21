# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `0a37b0bf9d796f268c056ce6bbdb5424f9f7e25f`
- plateau counter: `5`
- round loop: `round 14/50`
- rounds remaining: `37`
- notes: `Node C build succeeded for round 14/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_193817_bf16_gemm_v1_0a37b0b`
- run dir: `runs/20260420_193817_bf16_gemm_v1_0a37b0b`
- correctness: `PASS`
- median runtime: `25.504256 ms`
- TFLOP/s: `28.505808 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_193848`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 14/50 human-review audit: `state/human_review.md` currently contributes only the approval/selection gate and no extra user-authored idea family, so the ranking is driven by measured evidence alone. Accepted for this round: continue from the restored accepted dispatch baseline, because the latest run recovered the correct `128x128` hot-band branch and improved from `34.016768 ms` to `25.504256 ms`, already moving back under the CUTLASS runtime. Rejected as the primary family: the flat full-band `64x384` route remains closed negative after the prior `34.016768 ms` regression. Deferred: tiny cleanup-kernel work on the residual `64x384` band or the `64x96` tail, because the latest comparison to `1181247` shows the remaining gap is still best explained by the dominant `128x128` hot-band kernel rather than the small cleanup kernels. Primary idea family for the next loop: stage cadence/feed overlap on the accepted `128x128` hot-band path, with `128x128x32` ranked first because it preserves the accepted geometry while giving the largest bounded lever on the remaining hot-band gap.`
- dir_01: Activate 128x128x32 Two-K Hot-Band Staging | bottleneck: Hot-band stage cadence and feed overlap in the accepted `128x128` branch, not dispatch selection or the already-rejected full-band `64x384` family.
- dir_02: Retune K16 Copy Cadence In The Active 128x128 Kernel | bottleneck: A small long-scoreboard and feed-latency gap inside the active K16 `128x128` hot-band loop.
- dir_03: Bounded A/B Recheck Of The 128x128 PTX Microkernel Path | bottleneck: Hot-band export and instruction-mix overhead in the standard `128x128` kernel, addressed via the PTX microkernel's different store path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.495424 ms`, `0.942301x` slower than CUTLASS
