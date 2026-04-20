# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `3713ac4a81a442594f565309bb52b84291b0e391`
- plateau counter: `4`
- round loop: `round 52/100`
- rounds remaining: `49`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 52/100.`

## Latest measured custom run

- run id: `20260420_081140_bf16_gemm_v1_3713ac4`
- run dir: `runs/20260420_081140_bf16_gemm_v1_3713ac4`
- correctness: `PASS`
- median runtime: `25.716736 ms`
- TFLOP/s: `28.270284 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_081325`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `- round 52/100 must stay anchored to the accepted best base from round 47: `grouped-row=8 + K16` at `25.529328 ms` (`20260420_074331_bf16_gemm_v1_17a33b2`).
- round 48's B-fragment lookahead branch is explicit negative evidence and stays stopped: it regressed to `25.759745 ms`, so do not reopen extra-live-B or rolling-window Ps2r work.
- round 49's K32 cadence branch is also explicit negative evidence and stays stopped: it collapsed to `31.728224 ms`, so do not reopen another stage-width pivot.
- round 50 / 51 recovery clarified the branch boundary: `#pragma unroll 1` improved the stall mix but was not an accepted base, and restoring the active PTX path to `unroll 2` brought runtime back to `25.716736 ms`, still about `0.19 ms` slower than the accepted best.
- That means the next directions must build on accepted `grouped-row=8 + K16 + unroll2 + no-lookahead + single-scratch export`, not on the disproved lookahead or K32 variants and not on `unroll 1` as a new base.
- The latest run is still underfed rather than DRAM-bound: tensor active `48.22%`, warps active `16.65%`, L2 throughput `30.66%`, DRAM throughput `10.35%`, barrier `7.21%`, mio_throttle `4.78%`, short_scoreboard `1.93%`, long_scoreboard `1.31%`.
- Coalescing Access: not the lead family now; the 16-byte `cp.async` path and low DRAM utilization say the major coalescing win is already captured.
- Data Reuse: still valid because grouped-row=8 is the accepted base, but only as a narrow within-branch reuse or ordering refinement rather than a fresh branch.
- Async Copy: already present and useful; the next move is to retime the existing `cp.async` wait or commit handoff inside the accepted K16 path, not add another producer-side mechanism.
- Bank Conflict: still worth a third-ranked micro-probe because shared-side pressure can still leak into `mio_throttle`, but only via minimal layout or padding tweaks on the accepted surface.
- L2 Cache: still relevant because grouped-row locality produced the best run and current L2 is still around `30.66%`, but locality work must remain narrow and preserve grouped-row=8.
- Register Reuse: still a live family because round 51 is on the restored single-scratch path yet remains about `0.19 ms` slower than the accepted best; focus on A-fragment or export lifetime, not extra B residency.
- Pg2s: not the current limiter; DRAM stayed low enough that another global-to-shared rewrite is not the best use of this round.
- Ps2r: explicit stop for the B-fragment lookahead family after round 48; any remaining reuse work must avoid keeping another B fragment live.
- Stage: explicit stop for the K32 cadence family after round 49; the only valid stage work now is a small K16 handoff retime while keeping `unroll 2` and the accepted double buffer.
- Target framing stays unchanged: the user goal is still `<20 ms`, not merely staying ahead of CUTLASS.`
- dir_01: Keep The Accepted Unroll2 K16 Base And Retime The Existing Feed Or Issue Handoff | bottleneck: Feed or issue cadence and K16 stage-turnover latency inside the dominant 128x128 PTX hot-band microkernel, not raw DRAM bandwidth.
- dir_02: Trim Operand And Export Lifetime On The Accepted Single-Scratch PTX Surface | bottleneck: Register reuse or live-range pressure and export-side synchronization overhead inside the accepted PTX hot band, which may still be suppressing warp readiness after locality already improved.
- dir_03: Preserve The Accepted Base And Probe One Narrow Grouped-Row Or Shared-Mapping Micro-Tweak | bottleneck: Residual L2 reuse and shared-memory layout friction in the accepted grouped-row=8 PTX hot band, expressed more as MIO or bank-side inefficiency than as global-memory saturation.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-0.388560 ms`, `0.985008x` slower than CUTLASS
