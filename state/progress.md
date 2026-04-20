# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `a4646fcde92b3595f4801eb30c4e0026914da3a1`
- plateau counter: `2`
- round loop: `round 19/50`
- rounds remaining: `32`
- notes: `Node C build succeeded for round 19/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_000122_bf16_gemm_v1_a4646fc`
- run dir: `runs/20260420_000122_bf16_gemm_v1_a4646fc`
- correctness: `PASS`
- median runtime: `31.673856 ms`
- TFLOP/s: `22.953297 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_000335`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 19: Register Reuse becomes the primary family because the last two rounds showed that increasing shared-memory footprint is what killed active warps, while the 128x128 K16 branch already has the best stage/data-reuse balance. Async Copy, Data Reuse, Pg2s, Ps2r, and Stage remain accepted background choices because the winning kernel depends on them; the point now is to preserve that machinery while giving the compiler a chance to reduce live register pressure. Tiling 256x128 and deeper multi-stage overlap are deferred after two measured regressions. Coalescing Access and Bank Conflict are still deferred because the better and worse runs are not separating primarily on those signals. The L2 clue remains deferred but stays on the board as the next orthogonal axis if CTA-local occupancy tuning stalls.`
- dir_01: Restore the 128x128 K16 winner and add a register-pressure / launch-bounds hint to chase higher occupancy | bottleneck: Register-limited occupancy in the accepted 128x128 K16 hot-band kernel. The target is to increase resident blocks or at least reduce register pressure enough to lift warps active and tensor active.
- dir_02: Keep the 128x128 K16 base and tighten the consume fence only where overwrite actually occurs | bottleneck: Barrier overhead in the accepted 128x128 K16 mainloop.
- dir_03: Hold the CTA-local kernel fixed and try the deferred L2-friendly block-order clue | bottleneck: Inter-CTA cache locality rather than within-CTA tensor feed.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.287104 ms`, `1.126828x` slower than CUTLASS
