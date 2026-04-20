# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `7f0af836fe07d39be9f5b7354aadb7e740dbab6b`
- plateau counter: `4`
- round loop: `round 9/30`
- rounds remaining: `22`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 9/30.`

## Latest measured custom run

- run id: `20260419_222209_bf16_gemm_v1_7f0af83`
- run dir: `runs/20260419_222209_bf16_gemm_v1_7f0af83`
- correctness: `PASS`
- median runtime: `30.386592 ms`
- TFLOP/s: `23.925665 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_222312`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9/30 starts from the restored pre-sweep surface. The hot-band kernel still dominates, the warp-local consumer variants and CTA-order clue are both negative, and the previous stage-peeling attempt failed correctness. That leaves the copy pipeline as the clearest remaining human-idea family to test. Recommended direction dir_01 therefore tries a bounded ownership split inside the existing two-stage hot-band copy path: lower warps stage A, upper warps stage B, while all warps still participate in compute. Dir_02 is the restore fallback if that schedule fails quickly, and dir_03 records that steady-state peeling should only be revisited after the copy schedule becomes easier to reason about.`
- dir_01: Human idea async copy: split hot-band copy ownership so lower warps stage A and upper warps stage B | bottleneck: Global-to-shared staging issue regularity and LSU pressure in the hot-band copy phase.
- dir_02: Restore-only fallback if split ownership fails quickly | bottleneck: Not a direct bottleneck attack; this is a branch repair fallback.
- dir_03: Human idea stage: revisit steady-state peeling later, but only on a simpler copy schedule | bottleneck: Fixed-shape stage-transition overhead once the staging schedule itself is cleaner.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.514943 ms`, `1.135618x` slower than CUTLASS
