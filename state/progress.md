# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `046f075e6e6bba834990615cddaf89a3060fb4f1`
- plateau counter: `5`
- round loop: `round 44/100`
- rounds remaining: `57`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 44/100.`

## Latest measured custom run

- run id: `20260420_021058_bf16_gemm_v1_046f075`
- run dir: `runs/20260420_021058_bf16_gemm_v1_046f075`
- correctness: `PASS`
- median runtime: `30.126080 ms`
- TFLOP/s: `24.132560 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_021122`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `1. Round 43 is a negative result for deeper PTX hot-band staging: the K32 staged branch cut barrier from 11.18% to 4.80%, but runtime regressed from 27.003904 ms to 30.126080 ms, tensor active fell from 47.86% to 43.84%, `mio_throttle` rose from 0.56% to 2.37%, and `long_scoreboard` rose from 1.29% to 4.35%. Next rounds must judge ideas by wall-clock time plus tensor active together, not by barrier alone.
2. Coalescing Access: still live, but only as part of a measured hot-band locality/traversal or B-load packing change; it is not strong enough as a standalone target after the latest regression.
3. Data Reuse: still live because the PTX hot-band branch likely left reuse on the table when L2 throughput slipped; grouped-row scheduling and better hot-band traversal remain the cleanest reuse probe.
4. Async Copy: current negative result when expressed as a deeper K32 staged PTX pipeline on this branch; do not rank more async-stage expansion as the next move.
5. Bank Conflict: possible secondary contributor through the B shared layout or export scratch, but it should be bundled with reuse/layout work rather than treated as the primary diagnosis.
6. L2 Cache: still worth probing through grouped-row traversal and hot-band scheduling because the regressed run lost some L2 throughput while also losing tensor activity.
7. Register Reuse: promoted to the top family because the staged regression increased hot-band register pressure and shared allocation while lowering tensor issue efficiency.
8. Pg2s: not the next recommendation; producer-side staging already failed to translate barrier relief into speed, so further producer/deeper-stage work is currently deprioritized.
9. Ps2r: promoted ahead of more Stage work because the new stall mix points to fragment feed timing inside the PTX MMA microkernel.
10. Stage: explicitly treat deeper stage expansion as a current reject on this branch until a future idea can improve runtime and tensor active together.
11. The optimization target remains below 20 ms for the fixed benchmark, not merely re-matching or barely beating the 25.917889 ms CUTLASS baseline.`
- dir_01: Trim PTX Hot-Band Register And Export Lifetime | bottleneck: Register pressure and export-side live-range bloat in the active PTX hot-band branch are suppressing active warps and tensor issue efficiency after the failed K32 stage expansion.
- dir_02: Add A Small PTX Ps2r Lookahead Without Deeper Staging | bottleneck: Shared-to-register fragment feed latency and issue ordering in the PTX hot-band microkernel are now more limiting than CTA barrier frequency.
- dir_03: Recover Hot-Band Reuse Via Traversal And Shared-Layout Retune | bottleneck: Hot-band locality, cache reuse, and residual shared-layout friction are leaving the PTX branch underfed even after barrier was reduced.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `0.056383 ms`, `1.002175x` slower than CUTLASS
