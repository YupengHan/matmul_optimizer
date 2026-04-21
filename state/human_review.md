# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 13/50` with `38` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_193146`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 13/50 human-review audit: `state/human_review.md` currently contributes only the approval/selection gate and no extra user-authored idea family, so the diagnosis must explicitly accept, defer, or reject families from measured evidence alone. Rejected as the primary family for this round: the sweep-backed full-hot-band `64x384` route, because the latest run `20260420_193054_bf16_gemm_v1_acb0976` regressed to `34.016768 ms` and its main kernel shifted to `55.57%` DRAM throughput with `16.81%` barrier stalls, versus the accepted `1181247` base at `24.422464 ms` whose dominant `128x128` hot-band kernel sat at `12.84%` DRAM and `5.58%` barrier. Accepted for the next move: keep the restored accepted-base `128x128` hot-band family as the primary branch and make that dispatch reproducible. Deferred: tail-only cleanup, because the latest failure is dominated by the full-band main kernel rather than the `64x96` tail. Tertiary only: salvage the `64x384` family with a smaller internal live set if the restored-base branch later stalls.`
- dir_01: Re-Lock The Accepted 128x128 Default Dispatch | bottleneck: Dispatch/configuration drift into the negative full-band `64x384` path, which turns the hot kernel from a compute-balanced `128x128` branch into a DRAM- and barrier-heavy main kernel.
- dir_02: Activate The Dormant 128x128x32 Hot-Band Pipeline | bottleneck: Hot-band stage cadence and synchronization on the accepted `128x128` branch, not the full-band tile-routing family that just regressed.
- dir_03: If 64x384 Returns, Shrink Its Live Set Instead Of Reusing The Flat Sweep | bottleneck: Excess live B/accumulator state and memory pressure inside the peeled `64x384` hot-band kernel, not the tail kernel or the accepted `128x128` branch.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
