# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `91e446eea2cf2de912e81e21c45653dcd227d591`
- plateau counter: `0`
- round loop: `round 6/20`
- rounds remaining: `15`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 6/20.`

## Latest measured custom run

- run id: `20260418_225901_bf16_gemm_v1_91e446e`
- run dir: `runs/20260418_225901_bf16_gemm_v1_91e446e`
- correctness: `PASS`
- median runtime: `54.136911 ms`
- TFLOP/s: `13.429274 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_225935`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Replace the simple B-row skew with a warp-friendly shared-memory B swizzle | bottleneck: Shared-memory and MIO pressure on the B fragment load path inside the steady-state tensor loop
- dir_02: Retune the cp.async pipeline so the 4-warp CTA pays fewer full-block wait/sync penalties | bottleneck: Synchronization-limited overlap between async staging and MMA consumption in the steady-state mainloop
- dir_03: Bypass the shared epilogue scratch with a register-first BF16/vector store path | bottleneck: Epilogue LSU/MIO pressure and shared-footprint overhead from the `c_shared` round-trip

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `28.219023 ms`, `2.088786x` slower than CUTLASS
