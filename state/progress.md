# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `4784c8dad3001272fc9bd5ac33581f8a9bde6129`
- plateau counter: `96`
- round loop: `round 5/100`
- rounds remaining: `96`
- notes: `Node C build succeeded for round 5/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_114147_bf16_gemm_v1_4784c8d`
- run dir: `runs/20260421_114147_bf16_gemm_v1_4784c8d`
- correctness: `PASS`
- median runtime: `46.509056 ms`
- TFLOP/s: `15.631782 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_114422`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5/100 diagnosis emitted after recognizing that the historical accepted base is stale under the latest workload.`
- dir_01: Re-anchor on the best measured PTX surface under the current workload | bottleneck: Current-workload re-anchoring step; establishes the local PTX baseline before the next bounded barrier exploit.
- dir_02: After re-anchoring, retime the PTX barrier handoff on the 198-register surface | bottleneck: synchronization_barrier_issue on the current-workload 198-register PTX surface
- dir_03: Keep the 256x128 half-panel repair alive behind the new local anchor | bottleneck: occupancy_latency_hiding_issue on the wide geometry, with secondary barrier sensitivity

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
