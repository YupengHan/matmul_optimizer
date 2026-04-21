# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `7296bf25f5a6755c32d0c67ad96bec82369f14bf`
- plateau counter: `20`
- round loop: `round 33/100`
- rounds remaining: `68`
- notes: `Node C is ready to implement diagnosis_20260421_014129:dir_01 via recommended selection for round 33/100.`

## Latest measured custom run

- run id: `20260421_014052_bf16_gemm_v1_7296bf2`
- run dir: `runs/20260421_014052_bf16_gemm_v1_7296bf2`
- correctness: `PASS`
- median runtime: `26.398208 ms`
- TFLOP/s: `27.540484 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_014129`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 33 groups the PTX and non-PTX 128x128 launch-bounds probes into one coherent negative family. Both branches reached about 168 registers, about 24.7% active warps, and about 3 CTA residency, and both regressed because barrier stall climbed to about 11%. The x32 follow-on also already showed that doubling shared memory to amortize those barriers is not acceptable. The right move now is to restore the exact PTX anchor and then spend the next aggressive budget on true barrier surgery or on the broader 256x128 low-register branch, not on another launch-bounds replay.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Known register-limited plateau on the accepted PTX hot-band surface, used here as a recovery anchor.
- dir_02: Trim PTX Microkernel Barriers Without Reintroducing Shared-Memory Blowup | bottleneck: Barrier cadence inside the single-K PTX microkernel after the residency experiments exposed synchronization as the real limiting cost.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and synchronization strategy on the 256x128 path, plus correctness-sensitive writer ownership.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
