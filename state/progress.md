# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `6b518acb290f307ada1e207a9121a440e36edbbe`
- plateau counter: `4`
- round loop: `round 43/100`
- rounds remaining: `58`
- notes: `Node C build succeeded for round 43/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_020244_bf16_gemm_v1_6b518ac`
- run dir: `runs/20260420_020244_bf16_gemm_v1_6b518ac`
- correctness: `PASS`
- median runtime: `27.003904 ms`
- TFLOP/s: `26.922752 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_020307`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Current diagnosis assumes the active PTX hot-band path in src/kernels/bf16_gemm_v1.cu is already equivalent to accepted round-38 commit e26d834 on the active path; the user-verified diff says only formatting differs there, so round 42's 27.003904 ms fallback should be treated primarily as measurement drift / environment variance, not as a source-restore failure. NCU still points at the active 128x128 PTX hot-band microkernel as the optimization target: it dominates profiled time, reaches only 47.86% tensor-pipe activity, sits at 16.52% active warps, carries 11.18% barrier stall, and uses 188 registers per thread. Ranking therefore stays within the human idea families Async Copy / Stage, Register Reuse, and L2 Cache / Bank Conflict / Coalescing Access. The optimization target remains sub-20 ms for the fixed benchmark, not merely re-matching or barely beating the 25.917889 ms CUTLASS baseline.`
- dir_01: Retune PTX Hot-Band Async Stage | bottleneck: Synchronization and stage-pipeline overhead in the active hot-band PTX branch.
- dir_02: Trim Hot-Band Register Footprint | bottleneck: Register pressure and low active-warps occupancy in the active PTX hot-band branch.
- dir_03: Recover L2 And Shared-Layout Efficiency In Hot Band | bottleneck: L2 reuse loss plus residual shared-bank/layout friction in the active hot-band branch.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `0.056383 ms`, `1.002175x` slower than CUTLASS
