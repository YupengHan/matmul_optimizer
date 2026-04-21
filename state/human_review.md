# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 2/50` with `49` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_175514`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2/50 diagnosis for run `20260420_175429_bf16_gemm_v1_134ec64`. No new explicit human-review idea family is queued in `state/human_review.md`, so the ranking is driven by the latest measured regression and the already-measured fallback evidence on this loop. The key fact is that the regressed run came from the K32 hot-band branch, while the implementation surface has already been restored to the accepted `da1a5bb` PTX microkernel before this diagnosis. The latest run therefore acts as negative evidence: the K32 hot-band kernel drove the dominant kernel time from 32.97 ms to 39.57 ms, raised registers from 200 to 212, doubled hot-band shared memory from 22.016 KiB to 43.008 KiB, cut tensor activity from 47.72% to 40.05%, and pushed barrier stall from 5.52% to 10.04%. That closes the K32 family for the next round. The next directions should stay on the restored accepted surface and rank the surviving measured fallback families by upside versus risk: first the 4-row PTX grouping window as the best measured PTX-adjacent fallback, then the known 6144 seam as the best launch-split fallback, and only then the broad 64x384 fixed-main control because its local autotune evidence is outweighed by its catastrophic regression on the current PTX base.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: CTA grouping and orchestration overhead around the accepted PTX hot-band grouped-row mapping, not the hot-band inner K-stage itself.
- dir_02: Restore The 6144 Hot-Band / Peeled Seam As The Best Launch-Split Fallback | bottleneck: Boundary cost between the accepted 128x128 PTX hot-band launch and the peeled 64x384 row-band path, especially whether the fixed 6400-row split leaves a small but repeatable handoff penalty.
- dir_03: Keep The 64x384 Fixed-Main Control Only As A Broad Audit Branch | bottleneck: Broader hot-band path selection and arithmetic-intensity tradeoff across the fixed-shape launch, not PTX hot-band orchestration on the restored accepted surface.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
