# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `134ec64690b95b0a420b5463414213e1ecff17f7`
- plateau counter: `44`
- round loop: `round 2/50`
- rounds remaining: `49`
- notes: `Node C build succeeded for round 2/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_175429_bf16_gemm_v1_134ec64`
- run dir: `runs/20260420_175429_bf16_gemm_v1_134ec64`
- correctness: `PASS`
- median runtime: `30.297600 ms`
- TFLOP/s: `23.995941 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_175514`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2/50 diagnosis for run `20260420_175429_bf16_gemm_v1_134ec64`. No new explicit human-review idea family is queued in `state/human_review.md`, so the ranking is driven by the latest measured regression and the already-measured fallback evidence on this loop. The key fact is that the regressed run came from the K32 hot-band branch, while the implementation surface has already been restored to the accepted `da1a5bb` PTX microkernel before this diagnosis. The latest run therefore acts as negative evidence: the K32 hot-band kernel drove the dominant kernel time from 32.97 ms to 39.57 ms, raised registers from 200 to 212, doubled hot-band shared memory from 22.016 KiB to 43.008 KiB, cut tensor activity from 47.72% to 40.05%, and pushed barrier stall from 5.52% to 10.04%. That closes the K32 family for the next round. The next directions should stay on the restored accepted surface and rank the surviving measured fallback families by upside versus risk: first the 4-row PTX grouping window as the best measured PTX-adjacent fallback, then the known 6144 seam as the best launch-split fallback, and only then the broad 64x384 fixed-main control because its local autotune evidence is outweighed by its catastrophic regression on the current PTX base.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: CTA grouping and orchestration overhead around the accepted PTX hot-band grouped-row mapping, not the hot-band inner K-stage itself.
- dir_02: Restore The 6144 Hot-Band / Peeled Seam As The Best Launch-Split Fallback | bottleneck: Boundary cost between the accepted 128x128 PTX hot-band launch and the peeled 64x384 row-band path, especially whether the fixed 6400-row split leaves a small but repeatable handoff penalty.
- dir_03: Keep The 64x384 Fixed-Main Control Only As A Broad Audit Branch | bottleneck: Broader hot-band path selection and arithmetic-intensity tradeoff across the fixed-shape launch, not PTX hot-band orchestration on the restored accepted surface.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
