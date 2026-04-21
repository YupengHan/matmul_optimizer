# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `0a37b0bf9d796f268c056ce6bbdb5424f9f7e25f`
- plateau counter: `5`
- round loop: `round 14/50`
- rounds remaining: `37`
- notes: `Node A completed round 13/50. Run node_b to continue round 14/50.`

## Latest measured custom run

- run id: `20260420_193817_bf16_gemm_v1_0a37b0b`
- run dir: `runs/20260420_193817_bf16_gemm_v1_0a37b0b`
- correctness: `PASS`
- median runtime: `25.504256 ms`
- TFLOP/s: `28.505808 TFLOP/s`
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
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.495424 ms`, `0.942301x` slower than CUTLASS
