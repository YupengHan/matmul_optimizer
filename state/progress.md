# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `awaiting_direction_selection_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `16a98f7af190c1b90503973135cbf4b754cdad0a`
- plateau counter: `0`
- round loop: `round 1/5`
- rounds remaining: `5`
- notes: `Node B completed. Approve a direction or explicitly use the recommended direction before node_c.`

## Latest measured custom run

- run id: `20260419_015554_bf16_gemm_v1_16a98f7`
- run dir: `runs/20260419_015554_bf16_gemm_v1_16a98f7`
- correctness: `PASS`
- median runtime: `37.285807 ms`
- TFLOP/s: `19.498557 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_092350`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/5 diagnosis prepared from run 20260419_015554_bf16_gemm_v1_16a98f7. Recommended dir_01 per human-priority override; dir_01 and dir_02 are human ideas.`
- dir_01: Two-level B staging for the 64x384 hot band | bottleneck: Shared/L1 B-feed pressure and LSU issue bandwidth in the hot 64x384 kernel.
- dir_02: Phased 64x384 micro-panels to shrink the live set | bottleneck: Register-limited occupancy and weak latency hiding from keeping the full 384-wide working set live per warp.
- dir_03: Warp-specialized producer-consumer pipeline for the 64x384 loop | bottleneck: Synchronization and stage-orchestration overhead in the hot K-loop rather than raw DRAM bandwidth.

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `11.367918 ms`, `1.438613x` slower than CUTLASS
