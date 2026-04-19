# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `662a03b3908edf72485e5b57055242944802fa97`
- plateau counter: `1`
- round loop: `round 12/20`
- rounds remaining: `9`
- notes: `Node C build succeeded for round 12/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_000651_bf16_gemm_v1_662a03b`
- run dir: `runs/20260419_000651_bf16_gemm_v1_662a03b`
- correctness: `PASS`
- median runtime: `44.082689 ms`
- TFLOP/s: `16.492175 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_000749`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Aggressive exploration round 12/20 with human-in-loop guidance: do not recycle the round-11 producer/consumer cp.async path unchanged; prefer the recommended structural pivot from restored base 01d0040 unless a human explicitly approves a higher-risk alternative.`
- dir_01: Stage 32-wide K macro-tiles so each sync feeds two MMA slices | bottleneck: Tensor-core underfeed from too little MMA per staging/synchronization episode in the fixed-shape main loop.
- dir_02: Replace the WMMA row-major feed path with ldmatrix/mma.sync plus a tensor-core swizzle | bottleneck: Hot-path instruction mix and shared-fragment feed overhead that underfeeds tensor issue even when data is resident.
- dir_03: Split or eliminate the c_shared epilogue round-trip | bottleneck: Epilogue-side scalar, shared-memory, and MIO work polluting the tensor kernel's instruction mix.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `17.779776 ms`, `1.686004x` slower than CUTLASS
