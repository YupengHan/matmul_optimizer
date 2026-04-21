# Progress

## Objective

Beat cuBLAS and drive the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1` to `<= 18.000 ms`.
- target runtime: `<= 18.000 ms`
- comparison target: `cuBLAS`
- rebootstrap source: `20260420_235922_bf16_gemm_v1_489574e`, commit `489574ed5013268dbb79c634450d9a60155a294a`, historical runtime `24.164272 ms`

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `c859cd06456e600a76778265983f0cd6da925481`
- plateau counter: `1`
- round loop: `single-run`
- rounds remaining: `0`
- notes: `Node A completed. Run node_b to produce exactly three directions from the latest measured summaries.`

## Latest measured custom run

- run id: `20260421_133418_bf16_gemm_v1_c859cd06`
- run dir: `runs/20260421_133418_bf16_gemm_v1_c859cd06`
- correctness: `PASS`
- median runtime: `24.407552 ms`
- TFLOP/s: `29.786659 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `pending_generation`
- diagnosis id: `None`
- recommended direction: `None`
- approved direction: `None`
- diagnosis notes: `Run node_b to produce exactly three directions from the latest measured run.`
- no directions recorded yet

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve, use-recommended-direction, or select-next after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` of CUTLASS runtime (faster)
- cuBLAS median runtime: `22.289920 ms`
- current best custom gap vs cuBLAS: `1.874352 ms`, `1.084090x` of cuBLAS runtime (slower)
