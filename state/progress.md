# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `edcdbea324dc7306e7a111e771f8d65aaf39eabd`
- plateau counter: `5`
- round loop: `round 10/30`
- rounds remaining: `21`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 10/30.`

## Latest measured custom run

- run id: `20260419_222503_bf16_gemm_v1_edcdbea`
- run dir: `runs/20260419_222503_bf16_gemm_v1_edcdbea`
- correctness: `PASS`
- median runtime: `30.861776 ms`
- TFLOP/s: `23.557277 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_222558`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 10/30 starts from the clearest negative branch in several rounds. Splitting copy ownership across half the CTA spiked registers and both major staging stalls while slowing the dominant hot-band kernel, so there is no value in refining it. Recommended direction dir_01 therefore restores the pre-split surface immediately. Dir_02 records the next orthogonal family to try after that restore: trimming the hot-band export path instead of touching the copy path again. Dir_03 is a stricter baseline re-anchor if measurement drift remains confusing.`
- dir_01: Restore the restored best surface and discard the split-ownership staging branch | bottleneck: Not a new bottleneck attack; this is a branch reset after a strongly negative staging-ownership experiment.
- dir_02: After the restore, trim the hot-band export path instead of the copy path | bottleneck: Hot-band epilogue / export LSU and shared-memory round-trip overhead.
- dir_03: Re-anchor the loop explicitly at the recorded best custom measurement `5dd9f0d` | bottleneck: Workflow / baseline drift rather than a specific micro-bottleneck.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.514943 ms`, `1.135618x` slower than CUTLASS
