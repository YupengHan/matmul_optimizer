# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `b13027cdde2a90d1f00f3bd9b1e6b355ea15f2d9`
- plateau counter: `0`
- round loop: `round 16/20`
- rounds remaining: `5`
- notes: `Node C build succeeded for round 16/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_191708_bf16_gemm_v1_b13027c`
- run dir: `runs/20260419_191708_bf16_gemm_v1_b13027c`
- correctness: `PASS`
- median runtime: `30.052768 ms`
- TFLOP/s: `24.191430 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_191757`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 16 is a continue-family move on the Human idea 1 / Tiling branch, not a pivot away from it. The 256x128 CTA / 64x64 warp structural pivot is still the only family that has produced multi-millisecond step changes, and round 15 still set a new accepted base. The key diagnostic point this round is why barrier fell so hard without a matching wall-clock gain. The hot kernel's machine state changed dramatically in the expected direction for synchronization cleanup: barrier dropped from 20.89 to 6.49, mio fell from 2.23 to 0.33, tensor active rose from 37.58 to 38.55, and the profiled hot-kernel time improved materially. But registers stayed pinned at 167, active warps stayed around 16.68, and the new pressure simply showed up elsewhere: LSU wavefronts rose from 28.75 to 34.45, bank reads rose from 6.42 to 8.98, and short-scoreboard stayed high at 6.74. That means the current helper-level retime already captured most of the easy barrier win. The real wall is still the unchanged live accumulator footprint and register-limited residency, so another small barrier-focused tweak is the wrong next move.

Human idea audit for round 16:
1. Tiling: accept-now as the active top-level family. The 256x128/64x64 path remains the only clearly proven mainline.
2. Coalescing Access: defer. DRAM throughput is only 17.16 and the hot path already uses wide async copies, so global coalescing is not the primary wall.
3. Data Reuse: accept-now as a lower-ranked family-consistent option. Export scratch reuse over dead B-shared storage is now technically meaningful, but it is not the first wall to attack.
4. Async Copy: accept-now only as established baseline infrastructure. The current bottleneck is no longer obvious global-to-shared latency.
5. Bank Conflict: accept-now and rank second. The row-pair helper exposed a new shared-load and bank-read tax that deserves a bounded local follow-up.
6. L2 Cache: reject-for-this-round. The hot kernel is not L2- or DRAM-bound.
7. Register Reuse: accept-now and rank first. Barrier cleanup already landed; the unchanged register wall is now the clearest next limiter.
8. Pg2s: defer. The global-to-shared pipeline is functioning and is not the main missing win.
9. Ps2r: defer. Long scoreboard remains tiny relative to the register and shared-load issues.
10. Stage: reject-for-this-round. With only five rounds left, there is no evidence that reopening a stage-family rewrite beats continuing the proven tiling branch.

Primary decision for this round: continue the Human idea 1 family, but shift the immediate lever to a more aggressive Human idea 7 register-cut implementation. The round-15 helper retime showed that barrier was not the final wall; round 16 should attack the accumulator and register footprint directly.`
- dir_01: Human idea 7 Register reuse: replace the full 64x64 accumulator set with two serial 64x32 half-panel passes | bottleneck: Register-limited occupancy and warp-local live-state pressure inside the 64x64 PTX microkernel, not headline CTA barrier frequency.
- dir_02: Human idea 5 Bank conflict: keep the row-pair schedule, but retune only the 64x64 branch's B-shared mapping and consume order | bottleneck: Shared-memory bank and LSU pressure in the 64x64 PTX branch after the row-pair helper removed much of the previous synchronization tax.
- dir_03: Human idea 3 Data reuse: keep paired export, but overlay its scratch onto dead terminal B-shared storage to reclaim overlap budget | bottleneck: Export-side shared-memory budget and late-kernel scratch residency that now persists even after the main barrier problem has been reduced.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
