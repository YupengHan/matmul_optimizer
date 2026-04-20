# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `92cecc34d4a3c3f2e9e71d077cd466f6effba291`
- plateau counter: `3`
- round loop: `round 51/100`
- rounds remaining: `50`
- notes: `Node C build succeeded for round 51/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_080414_bf16_gemm_v1_92cecc3`
- run dir: `runs/20260420_080414_bf16_gemm_v1_92cecc3`
- correctness: `PASS`
- median runtime: `26.128896 ms`
- TFLOP/s: `27.824345 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_080439`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `- grouped-row=8 + K16 from round 47 (`20260420_074331_bf16_gemm_v1_17a33b2`) remains the accepted best base at `25.529328 ms`.
- round 50 restored grouped-row=8 + K16 and set the active PTX main loop to `#pragma unroll 1`; runtime came back to `26.128896 ms`, still about `0.60 ms` slower than the accepted base.
- `#pragma unroll 1` is not the accepted base, but it exposed real feed or issue signal: `mio_throttle 5.81 -> 3.83`, `short_scoreboard 2.82 -> 0.71`, `lts 26.91 -> 30.97`, and `barrier 9.18 -> 7.18`.
- next round's highest-value attempt is `dir_01`: recover accepted-base throughput while keeping the improved stall mix via selective feed or issue retiming, not by promoting full `unroll 1`.
- Coalescing Access: not the lead family now; 16-byte async copies and the current access pattern already captured the large coalescing win.
- Data Reuse: still valid because grouped-row=8 remains the accepted base, but the scope is now a narrow within-branch reuse refinement rather than a broad new remap.
- Async Copy: already present and useful via `cp.async`; the next move should retime the existing mechanism, not invent another copy path.
- Bank Conflict: still worth a third-ranked micro-probe because shared-side friction can still leak into MIO pressure, but it is secondary to feed or issue retiming on the accepted base.
- L2 Cache: clearly still real because the accepted base came from grouped-row locality and round 50 lifted L2 further, but cache work should stay narrow and must preserve grouped-row=8 + K16.
- Register Reuse: still an active family, especially around operand and export lifetime, but do not reopen the disproved extra-live-B route.
- Pg2s: not the current limiter family; global-to-shared movement already looks competent enough that another producer-side rewrite is not the best next round.
- Ps2r: explicit caution family; keep any reuse work away from extra-live-B or rolling-window lookahead, because that branch already failed to hold the accepted base.
- Stage: still the most important family, but in the constrained K16 form of feed or issue cadence retuning inside the accepted microkernel, not as another K32 pivot and not by treating `unroll 1` as the new base.
- Target framing stays unchanged: the user goal is still `<20 ms`, not merely beating CUTLASS.`
- dir_01: Recover Accepted K16 Through Selective Feed/Issue Retiming | bottleneck: Feed/issue scheduling and K16 stage-turnover latency in the dominant grouped-row=8 128x128 PTX hot-band microkernel, not raw DRAM bandwidth.
- dir_02: Trim Operand And Export Lifetime On The Accepted PTX Surface | bottleneck: Operand lifetime and export-side issue pressure inside the grouped-row=8 PTX hot band, which may still be suppressing warp readiness after locality already improved.
- dir_03: Keep Grouped-Row=8 K16 And Probe One Narrow Locality Or Shared-Layout Refinement | bottleneck: Residual L2 locality and shared-layout friction in the accepted grouped-row=8 PTX hot band, expressed more as MIO or bank-side inefficiency than as raw global-memory saturation.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-0.388560 ms`, `0.985008x` slower than CUTLASS
