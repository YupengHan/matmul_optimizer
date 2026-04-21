# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `9144f92dd9a6f5b4f85ab4278581ccabe96eae93`
- plateau counter: `4`
- round loop: `round 7/50`
- rounds remaining: `44`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 7/50.`

## Latest measured custom run

- run id: `20260420_184055_bf16_gemm_v1_9144f92`
- run dir: `runs/20260420_184055_bf16_gemm_v1_9144f92`
- correctness: `FAIL`
- median runtime: `29.100464 ms`
- TFLOP/s: `24.983087 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_184122`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 7/50 diagnosis for 20260420_184055_bf16_gemm_v1_9144f92. Human-review audit: state/human_review.md currently contains only workflow-gate and approval-policy text, with no explicit user-supplied idea-family bullets to accept or reject one by one, so the ranking is evidence-driven rather than keyed to queued human ideas. Accepted for this round: correctness-preserving 128x128 control pivots that keep the grouped-row locality lesson from the accepted 2e4dd24 base while abandoning the broken wide-CTA auxiliary promotion; the primary family is dir_01. Deferred: another bounded retime inside the accepted grouped PTX handoff window, because that family has a strong historical floor (24.71358395 ms on 57d08c3) but already regressed once on the current grouped-rows-4 lineage (25.51500797 ms on e1c12b7). Rejected for this round: promoting the measured 256x128 auxiliary path as-is, because 9144f92 failed correctness 0/3 and its hot-band kernel regressed to 40.086 ms with 21.84% barrier stalls and only 39.55% tensor activity. Also rejected: reopening the broad fixed-main override family, because the old round-18 autotune sweep only proved 384 was the best option on the much older flat fixed-main surface, while newer current-regime validation runs ef8cb27 (33.59487915 ms) and a64854a (33.9645443 ms) show that family is far off the accepted 24.44441605 ms base.`
- dir_01: Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling | bottleneck: If the grouped-row port is incomplete, the sibling kernel will likely give back L2 reuse and shift the bottleneck from barrier stalls to long-scoreboard or memory-latency stalls. The target is lower barrier share without collapsing cache behavior relative to the accepted grouped PTX base.
- dir_02: Retune The Accepted PTX Handoff Window Without Reopening Wide CTA Paths | bottleneck: This branch is bounded by the current accepted base already being close to a local optimum. A retime that lowers one sync point can easily just move the stall budget from barrier to scoreboard or export/writeback without net runtime gain.
- dir_03: Quarantine The 256x128 Auxiliary Branch To Fix Barrier Tax And Correctness | bottleneck: The dominating bottleneck is synchronization, not raw register pressure. The explicit `__syncthreads()` cadence and shared staging contract are likely starving tensor issue, and the same sequencing may also be the source of the full correctness failure.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.473473 ms`, `0.943148x` slower than CUTLASS
