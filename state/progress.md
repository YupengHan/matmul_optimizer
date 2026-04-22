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
- latest measured commit: `4948b8ea197c9869356471fedefa11a45b84ee35`
- plateau counter: `21`
- round loop: `round 5/20`
- rounds remaining: `16`
- notes: `Node C build succeeded for round 5/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_183233_bf16_gemm_v1_4948b8ea`
- run dir: `runs/20260421_183233_bf16_gemm_v1_4948b8ea`
- correctness: `PASS`
- median runtime: `25.251841 ms`
- TFLOP/s: `28.790750 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_183411`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5 treats the 3-stage Pg2s probe as informative but incomplete: it fixed the long_scoreboard problem and slightly reduced registers, so the next move should clean up the handoff tax before discarding the family.`
- dir_01: Retune PTX Hot-Band Grouped Rows From 4 Down To 2 On The 3-Stage Surface | bottleneck: Grouped-row batching is likely over-amortizing locality on the 3-stage surface and paying extra barrier plus handoff delay per CTA group.
- dir_02: Split The Final 3-Stage PTX Drain Out Of The Late Steady-State Loop | bottleneck: Late-drain synchronization is now the most likely remaining local tax on the 3-stage surface.
- dir_03: Reopen 256x128 64x64-Warp Hot-Band Tiling On The Dominant Surface | bottleneck: The 128x128 PTX hot-band surface may be hitting a real tiling and reuse ceiling even after local pipeline cleanup.

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
