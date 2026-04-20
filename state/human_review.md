# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 43/100` with `58` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_020307`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Current diagnosis assumes the active PTX hot-band path in src/kernels/bf16_gemm_v1.cu is already equivalent to accepted round-38 commit e26d834 on the active path; the user-verified diff says only formatting differs there, so round 42's 27.003904 ms fallback should be treated primarily as measurement drift / environment variance, not as a source-restore failure. NCU still points at the active 128x128 PTX hot-band microkernel as the optimization target: it dominates profiled time, reaches only 47.86% tensor-pipe activity, sits at 16.52% active warps, carries 11.18% barrier stall, and uses 188 registers per thread. Ranking therefore stays within the human idea families Async Copy / Stage, Register Reuse, and L2 Cache / Bank Conflict / Coalescing Access. The optimization target remains sub-20 ms for the fixed benchmark, not merely re-matching or barely beating the 25.917889 ms CUTLASS baseline.`
- dir_01: Retune PTX Hot-Band Async Stage | bottleneck: Synchronization and stage-pipeline overhead in the active hot-band PTX branch.
- dir_02: Trim Hot-Band Register Footprint | bottleneck: Register pressure and low active-warps occupancy in the active PTX hot-band branch.
- dir_03: Recover L2 And Shared-Layout Efficiency In Hot Band | bottleneck: L2 reuse loss plus residual shared-bank/layout friction in the active hot-band branch.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
