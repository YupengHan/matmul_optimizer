# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `dfd7960585906ecd34e523003e3631dcd1bfd37b`
- plateau counter: `16`
- round loop: `round 1/30`
- rounds remaining: `30`
- notes: `Node C build succeeded for round 1/30. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_214535_bf16_gemm_v1_dfd7960`
- run dir: `runs/20260419_214535_bf16_gemm_v1_dfd7960`
- correctness: `PASS`
- median runtime: `32.758783 ms`
- TFLOP/s: `22.193114 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_215124`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/30 starts from a bad exploratory endpoint rather than a trustworthy optimization anchor. The latest measured branch (`dfd7960`) is correctness-stable but clearly negative: runtime regressed to 32.758783 ms, the hot-band kernel slowed to about 47.99 us, tensor active collapsed to about 33.2%, barrier stall jumped to about 27.97%, and registers exploded to about 222/thread. That means the minimal producer-only staging variant is not a viable baseline for another 29 rounds. The first move should therefore be a reset to a stronger implementation surface before spending more rounds on new ideas. Among recent branches, the restored round-8 streaming-B path is the best exploratory anchor because it was the last family with a clean positive feed-side signal while keeping registers and shared memory flat. Recommended direction dir_01 therefore restores the round-8 streaming-B implementation surface, re-establishes that branch as the working baseline, and only then resumes B-feed exploration. Dir_02 keeps the stronger global objective in view by offering a reset to the best measured custom commit, while dir_03 is the highest-ceiling direct follow-up once the streaming-B branch is restored.`
- dir_01: Restore the round-8 streaming-B branch before continuing exploration | bottleneck: Not a micro-bottleneck change; this is a branch reset to remove a clearly negative orchestration experiment and recover the last good B-feed baseline.
- dir_02: Reset to the best measured custom commit `b13027c` and re-anchor the loop there | bottleneck: Not a direct bottleneck attack; this is a global baseline reset to the best measured implementation surface.
- dir_03: After restoring round 8, add one-fragment Ps2r lookahead on the streaming-B path | bottleneck: Residual shared-to-register feed latency inside the hot-band 64x64 micro-tile after the round-8 consumer cleanup.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
