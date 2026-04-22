# Progress

## Objective

Beat cuBLAS and drive the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1` to `<= 18.000 ms`.
- target runtime: `<= 18.000 ms`
- comparison target: `cuBLAS`
- rebootstrap source: `20260420_235922_bf16_gemm_v1_489574e`, commit `489574ed5013268dbb79c634450d9a60155a294a`, historical runtime `24.164272 ms`

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `9e21c98f50fb159e6c01b4fecbe86beaaacf569a`
- plateau counter: `26`
- round loop: `round 10/20`
- rounds remaining: `11`
- notes: `Node C build succeeded for round 10/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_190032_bf16_gemm_v1_9e21c98f`
- run dir: `runs/20260421_190032_bf16_gemm_v1_9e21c98f`
- correctness: `PASS`
- median runtime: `24.841215 ms`
- TFLOP/s: `29.266661 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_190245`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 10 diagnosis emitted after the barrier-trim experiment regressed and should be cleared before the checkpoint.`
- dir_01: Restore The Accepted Compact PTX Cadence After The Failed Barrier Trim | bottleneck: This is a recovery direction rather than a new bottleneck theory; its purpose is to remove a falsified sync variant and return to the accepted compact PTX surface.
- dir_02: Reopen The Writer-Safe 256x128 64x64-Warp Hot-Band Branch From The Accepted PTX Base | bottleneck: The 128x128 PTX surface may still be constrained by geometry and warp-reuse limits once the local cadence is back on the accepted base.
- dir_03: Port The PTX Hot-Band Path To The Existing 2-K Pg2s Stage Schedule | bottleneck: Barrier, refill cadence, and latency hiding on the dominant hot-band path rather than raw DRAM bandwidth.

## Active implementation direction

- direction id: `dir_02`
- selection mode: `frontier`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` of CUTLASS runtime (faster)
- cuBLAS median runtime: `22.000000 ms`
- current best custom gap vs cuBLAS: `2.164272 ms`, `1.098376x` of cuBLAS runtime (slower)
