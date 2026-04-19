# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `awaiting_direction_selection_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `1e399d80f7b02720493e3275ecb2c6865cbe1e63`
- plateau counter: `0`
- round loop: `round 4/5`
- rounds remaining: `2`
- notes: `Node B completed. Approve a direction or explicitly use the recommended direction before node_c.`

## Latest measured custom run

- run id: `20260419_135930_bf16_gemm_v1_1e399d8`
- run dir: `runs/20260419_135930_bf16_gemm_v1_1e399d8`
- correctness: `PASS`
- median runtime: `33.366047 ms`
- TFLOP/s: `21.789199 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_140002`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `All three directions stay strictly inside the 64x384 hot-band PTX microkernel branch and keep the 64x96 tail unchanged. Ranking uses the new fact that round 3 pushed runtime down again to 33.366 ms while barrier and mio both dropped materially, so the branch should not change lines now. The remaining guardrail is still occupancy_limit_registers=1 with active warps stuck near 16.6, but the profile also shows compute-memory and DRAM throughput already much higher than before. That shifts ranking toward end-to-end PTX follow-through on export and full-width dataflow control, while explicitly avoiding the previously rejected explicit mma.sync half-panel subpath.`
- dir_01: Register-first PTX export follow-through on the hot band | bottleneck: The remaining cost has shifted away from barrier and mio tax toward export-side shared/LSU work and residual register lifetime in the hot-band epilogue.
- dir_02: Full-width explicit PTX load-order control without the regressed half-panel path | bottleneck: With barrier and mio now low, residual long-scoreboard and feed latency inside the PTX compute body are a more plausible limiter than orchestration tax.
- dir_03: PTX helper and lifetime compaction for the 12-tile accumulator set | bottleneck: Compiler-visible live-range inflation around the named 12-tile PTX helper surface is still contributing to the occupancy guardrail even after orchestration improvements.

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `7.448158 ms`, `1.287375x` slower than CUTLASS
