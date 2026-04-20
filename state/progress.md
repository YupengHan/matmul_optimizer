# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `1cfe45357c836d8da9abf495ede7a932733ec8a9`
- plateau counter: `19`
- round loop: `round 4/30`
- rounds remaining: `27`
- notes: `Node C build succeeded for round 4/30. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_220419_bf16_gemm_v1_1cfe453`
- run dir: `runs/20260419_220419_bf16_gemm_v1_1cfe453`
- correctness: `FAIL`
- median runtime: `30.270464 ms`
- TFLOP/s: `24.017452 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_220618`
- recommended direction: `dir_01`
- approved direction: `dir_02`
- diagnosis notes: `Round 4/30 starts from a run that is faster but invalid. The approved A-side Ps2r lookahead improved measured runtime from 30.592960 ms to 30.270464 ms and shortened the hot-band kernel from about 41.19 us to about 40.99 us, which means the underlying overlap idea may have real upside. At the same time, correctness failed on all three cases, registers ticked up again to about 168/thread, `launch__occupancy_limit_registers` stayed pinned at 1, barrier stall jumped to about 19.84%, and `mio_throttle` rose back to about 2.50. That profile does not justify continuing to layer new optimization ideas on top of the broken branch. Recommended direction dir_01 therefore focuses on repairing or falsifying the A-lookahead family itself: keep the same concept, but flatten the row-pair preload into an explicit fixed-shape implementation that avoids the current recursive fragment handoff. Dir_02 is the safe fallback restore to the last correct round-2 surface, and dir_03 preserves the user-provided L2 traversal clue for later once the branch is valid again.`
- dir_01: Repair the A-side lookahead as an explicit fixed-shape row-pair preload, then revalidate correctness | bottleneck: Implementation / codegen risk in the current A-side lookahead path, plus residual shared-to-register A-feed latency if the idea survives repair.
- dir_02: Restore the last correct round-2 branch `06eedc6` and continue from the validated streaming-B + B-lookahead surface | bottleneck: Not a direct micro-bottleneck attack; this is a branch repair to recover a correctness-valid baseline before the next experiment.
- dir_03: Human idea L2 cache clue: try a grouped CTA traversal only after the correctness path is stable again | bottleneck: Potential CTA traversal inefficiency and weak L2 locality across the hot-band grid once a correctness-valid branch is restored.

## Active implementation direction

- direction id: `dir_02`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
