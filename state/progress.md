# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `da1a5bbd4af452569659b4db75fff988f44084e0`
- plateau counter: `43`
- round loop: `round 1/50`
- rounds remaining: `50`
- notes: `Node C build succeeded for round 1/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_164612_bf16_gemm_v1_da1a5bb`
- run dir: `runs/20260420_164612_bf16_gemm_v1_da1a5bb`
- correctness: `PASS`
- median runtime: `25.476608 ms`
- TFLOP/s: `28.536743 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_174253`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/50 diagnosis for run 20260420_164612_bf16_gemm_v1_da1a5bb. No new explicit human-review idea family is queued in state/human_review.md. The latest implemented hybrid prefetch ordering improved runtime from 25.62406445 ms to 25.47660828 ms and cut hot-band barrier pressure from 6.63 to 5.52 while reducing registers from 202 to 200, but the dominant 128x128 PTX hot-band kernel still accounts for 32.97 ms, remains capped at two resident blocks with only 16.54% active warps, and traded that barrier win for worse long-scoreboard stall (5.60 to 8.02). That closes the prefetch-order family as the next primary move. The round-18 fixed-main autotune sweep is still useful as historical evidence that broader tile-width changes can matter, but on the current dedicated hot-band path the next step should stay inside the hot-band kernel family: first a staged 128x128x32 branch, then the simpler two-stage sibling as a control, with the previously measured 6144 seam held only as a tertiary audit fallback.`
- dir_01: Activate The Dormant 128x128x32 Hot-Band Branch | bottleneck: Synchronization and latency-hiding limits in the current 128x128 K16 hot-band cadence, especially the two-block occupancy ceiling and rising long-scoreboard stalls.
- dir_02: Use The Existing 128x128 Two-Stage Sibling As The Lower-Risk Control | bottleneck: Register pressure and helper-path latency inside the current hot-band PTX microkernel rather than raw DRAM bandwidth.
- dir_03: Restore The 6144 Hot-Band/Peeled Seam Only As An Audit Fallback | bottleneck: Boundary cost between the dominant 128x128 PTX hot-band launch and the peeled 64x384 follow-on band, not the hot-band inner microkernel.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
