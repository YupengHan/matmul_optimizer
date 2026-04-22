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
- latest measured commit: `49dfa799e322ba9331fa5ca20569d94830666c89`
- plateau counter: `19`
- round loop: `round 3/20`
- rounds remaining: `18`
- notes: `Node C build succeeded for round 3/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_182124_bf16_gemm_v1_49dfa799`
- run dir: `runs/20260421_182124_bf16_gemm_v1_49dfa799`
- correctness: `PASS`
- median runtime: `26.306592 ms`
- TFLOP/s: `27.636397 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_182251`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3 treats 49dfa799 as a local launch-policy regression on top of the compact PTX base, not as a reason to abandon the PTX hot-band family. The next move should isolate launch_bounds before reopening larger geometry or shared-memory families.`
- dir_01: Restore PTX Launch Bounds Back To 2-CTA On The Active Hot-Band Path | bottleneck: The explicit 3-CTA minimum is over-constraining the PTX microkernel schedule, inflating barrier and short-scoreboard even though it does not reduce the measured register footprint.
- dir_02: Split The Final PTX Wait/Sync Drain Out Of The Steady-State Loop | bottleneck: The final steady-state handoff is paying an unnecessary wait/sync pair that shows up as barrier and short-scoreboard tax on the PTX path.
- dir_03: Retune PTX Hot-Band Grouped Rows From 4 Down To 2 | bottleneck: PTX grouped-row batching may be over-amortizing locality and paying too much synchronization and scheduler delay per group.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `frontier`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` of CUTLASS runtime (faster)
- cuBLAS median runtime: `22.000000 ms`
- current best custom gap vs cuBLAS: `2.164272 ms`, `1.098376x` of cuBLAS runtime (slower)
