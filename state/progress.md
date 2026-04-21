# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `cb070a739eb38f4ea8ca9c5e0243a825338dbf67`
- plateau counter: `6`
- round loop: `round 15/50`
- rounds remaining: `36`
- notes: `Node C build succeeded for round 15/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_194440_bf16_gemm_v1_cb070a7`
- run dir: `runs/20260420_194440_bf16_gemm_v1_cb070a7`
- correctness: `PASS`
- median runtime: `31.797344 ms`
- TFLOP/s: `22.864155 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_195219`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 15/50 human-review audit: `state/human_review.md` currently contributes only the approval/selection gate and the exactly-one-direction rule, with no extra user-authored idea family queued. Accepted for this round: a single-family rollback away from the newly measured `128x128x32` hot-band staging path, because run `20260420_194440_bf16_gemm_v1_cb070a7` regressed from `25.504256 ms` to `31.797344 ms` and its dominant hot-band kernel rose to `212` regs/thread, `43,008` B shared/block, `10.06%` barrier stall, and `10.27%`/`5.03%` L1 bank read/write pressure while tensor activity fell to `39.88%`. Deferred: the older sweep-backed full-band `64x384` family from `state/autotune_round18_main_tiles.md`; it is still useful background, but direct node_a evidence already showed that reopening it on the restored surface regressed to `34.016768 ms`, so it is not the next move. Rejected as the primary family: any further deepening of the `128x128` stage pipeline, because the current two-K version is already the measured negative. Secondary fallback families kept open for approval are the one-K PTX `128x128` path and the existing `256x128` pivot hot-band path, each isolated as a single node_c change to respect the human-review gate.`
- dir_01: Re-Lock The Single-K 128x128 Hot-Band Default | bottleneck: Register-limited occupancy plus shared-memory/barrier pressure inside the two-K `128x128x32` hot-band kernel, not the residual `64x384` rows or the `64x96` tail.
- dir_02: Swap The Default To The 128x128 PTX One-K Microkernel | bottleneck: Hot-band export/store overhead and stage lifetime inside the current default branch, addressed by the PTX one-K microkernel rather than by deeper staging.
- dir_03: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Hot-band tile hierarchy and CTA-count overhead in the current `128x128x32` split, rather than deeper pipeline cadence alone.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.495424 ms`, `0.942301x` slower than CUTLASS
