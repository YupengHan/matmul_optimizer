# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `8eb3db3a5d67ccd595b8098ceae78ef28ec0a8b6`
- plateau counter: `1`
- round loop: `round 5/20`
- rounds remaining: `16`
- notes: `Node C build succeeded for round 5/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_221336_bf16_gemm_v1_8eb3db3`
- run dir: `runs/20260420_221336_bf16_gemm_v1_8eb3db3`
- correctness: `PASS`
- median runtime: `24.519168 ms`
- TFLOP/s: `29.651064 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_222244`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5/20 audit: round 4's grouped-CTA traversal probe regressed from 24.177664 ms to 24.519168 ms, while the active PTX hot-band kernel still shows the same basic signature: 200 registers/thread, register-limited occupancy at 2 CTAs per SM, only 16.60% active warps, 48.36% tensor-pipe activity, and very low DRAM pressure. That rejects CTA traversal/locality as the primary family for the next round and puts the focus back on the PTX microkernel's control-path and live-range pressure. Because the recent search-policy update thinned the live queue, the ranking also pulls in two historically strong families from round_history: a register-pressure/helper-flattening branch and a restore of the best measured PTX grouping window. The 256x128 pivot family stays deferred after its earlier loss.`
- dir_01: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual PTX hot-band control-path overhead and live-range pressure inside the current 128x128 microkernel, not global bandwidth or another CTA-ordering miss.
- dir_02: Flatten PTX Hot-Band Compute Helpers To Reduce Register Pressure | bottleneck: Register-limited occupancy and weak latency hiding driven by helper structure and live-range expansion in the PTX hot-band compute path.
- dir_03: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Inter-CTA locality and launch-order mapping on the accepted PTX surface, but only as a historical restore fallback rather than the primary bottleneck attack.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.740225 ms`, `0.932856x` slower than CUTLASS
