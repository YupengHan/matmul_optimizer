# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `05bac60ebd99e273cb46db683c56f34d8cdd87fe`
- plateau counter: `6`
- round loop: `round 4/5`
- rounds remaining: `2`
- notes: `Node C build succeeded for round 4/5. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_124436_bf16_gemm_v1_05bac60`
- run dir: `runs/20260419_124436_bf16_gemm_v1_05bac60`
- correctness: `PASS`
- median runtime: `41.554512 ms`
- TFLOP/s: `17.495559 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_124517`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- diagnosis notes: `Diagnosed round-3 run 20260419_124436_bf16_gemm_v1_05bac60 while ranking against the restored accepted base 15d63b2 at 35.725824 ms. Round 1 warp specialization and round 3 straight-line producer scheduling are both strong negative evidence because both collapsed the hot kernel to one register-limited block per SM. The recommended direction therefore follows the human constraint set exactly: any new B-feed attempt must be warp-local at the consumer boundary only, with no CTA-wide repack, no second B shared tile, no extra CTA barrier, no increase in `launch__shared_mem_per_block_allocated`, and no reduction in `kCSharedStageCount`.`
- dir_01: Use a warp-local consumer-side B load swizzle on the peeled 64x384 hot path | bottleneck: Warp-local shared-memory B-fragment reads and bank behavior in the 64x384 hot kernel, where the current consumer path may still be overfeeding LSU without requiring any macro-tile or CTA-pipeline rewrite.
- dir_02: Pair Tile384 epilogue export across the existing two C-scratch stages | bottleneck: Hot-kernel shared export and LSU traffic after MMA completion, which can still contribute to the restored base's high mio_throttle even when occupancy is healthy.
- dir_03: Peel only the fixed final-drain path on the restored steady-state kernel | bottleneck: Terminal stage-drain control overhead in the hot kernel, with the main risk being a repeat of round 2 where barrier/mio improve but scoreboard pressure rises enough to lose runtime.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `8.737343 ms`, `1.337116x` slower than CUTLASS
