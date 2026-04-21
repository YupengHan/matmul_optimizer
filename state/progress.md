# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `3eed315e7f97652818bc8a8b129b4f977ac7613c`
- plateau counter: `99`
- round loop: `round 8/100`
- rounds remaining: `93`
- notes: `Node C build succeeded for round 8/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_122942_bf16_gemm_v1_3eed315`
- run dir: `runs/20260421_122942_bf16_gemm_v1_3eed315`
- correctness: `FAIL`
- median runtime: `43.250160 ms`
- TFLOP/s: `16.809635 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_123024`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 8/100 diagnosis emitted after a correctness-failing but highly promising 104-register PTX writer surface appeared.`
- dir_01: Repair the PTX writer row sweep while preserving the 104-register surface | bottleneck: correctness recovery on the PTX export/store path first; if preserved, the new steady-state signature becomes barrier-heavy and more memory-active rather than occupancy-limited
- dir_02: After the writer repair, retime the barrier seam on the 104-register anchor | bottleneck: synchronization_barrier_issue with secondary global_memory_bound behavior on the corrected 104-register PTX surface
- dir_03: Fallback: restore the last correct PTX writer semantics if the low-register repair collapses | bottleneck: fallback recovery to the last correctness-safe current-workload PTX writer surface

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
