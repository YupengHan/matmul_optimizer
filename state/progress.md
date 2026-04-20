# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `1d9b03ebc40198067f1bec2628b1bc01be67b4e8`
- plateau counter: `4`
- round loop: `round 63/100`
- rounds remaining: `38`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 63/100.`

## Latest measured custom run

- run id: `20260420_091028_bf16_gemm_v1_1d9b03e`
- run dir: `runs/20260420_091028_bf16_gemm_v1_1d9b03e`
- correctness: `PASS`
- median runtime: `25.281983 ms`
- TFLOP/s: `28.756424 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_091130`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Diagnosis anchored to run 20260420_091028_bf16_gemm_v1_1d9b03e at 25.281983 ms; exactly three ranked directions recorded for round 63/100.`
- dir_01: Restore accepted base, then retest finer issue granularity on the hot band | bottleneck: Issue granularity and instruction pressure inside the hot-band loop, not higher-level locality. The evidence suggests grouped_rows=4 is still slower than the accepted base and also raises DRAM to 13.05, while nearby consumer/refill variants remain negative.
- dir_02: Accepted base plus narrow overlap recovery behind the one-sync handoff | bottleneck: A short post-handoff gap rather than the broader locality structure. This is the smallest safe tweak after the accepted base is restored.
- dir_03: Small locality closure on the restored grouped_rows=8 base | bottleneck: Residual locality and reuse loss, but only as a secondary issue after the accepted base is back in place.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
