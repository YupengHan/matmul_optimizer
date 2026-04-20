# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `63d2fafdf1de4fcbc09b734f8f6f3a3320e8b1b7`
- plateau counter: `15`
- round loop: `round 10/10`
- rounds remaining: `1`
- notes: `Node C build succeeded for round 10/10. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_214140_bf16_gemm_v1_63d2faf`
- run dir: `runs/20260419_214140_bf16_gemm_v1_63d2faf`
- correctness: `PASS`
- median runtime: `30.856704 ms`
- TFLOP/s: `23.561150 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_214233`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Final-round audit after the round-9 regression and restore to the stronger round-8 implementation surface: Tiling remains accepted at the 64x384 hot-band shape; Coalescing Access, Data Reuse, Async Copy, and Pg2s remain baseline; L2 Cache, fixed-shape Stage, and the footprint-neutral B shared permutation are all now explicitly treated as tested-negative for this loop; the round-8 streaming B-consumer branch remains the best recent positive signal because it improved runtime and feed-side metrics without increasing registers or shared memory. That means the strongest remaining final-round bet is not another tiny B-layout permutation, but a more orthogonal complement on top of the restored round-8 feed branch. Recommended direction dir_01 therefore spends the last round on producer/consumer warp specialization over the round-8 streaming path: if the feed path is cleaner and the result is still occupancy-limited, the remaining upside is likely orchestration rather than another narrow layout tweak.`
- dir_01: Warp-specialized producer/consumer on top of the restored round-8 streaming B branch | bottleneck: All-warps staging and handoff overhead after the most obvious warp-local B feed pressure has already been reduced.
- dir_02: Human idea Ps2r on the restored round-8 streaming branch: one-fragment shared-to-register lookahead | bottleneck: Residual shared-to-register feed latency inside the hot-band 64x64 micro-tile after the round-8 consumer refactor.
- dir_03: Trim the hot-band export path so the feed-side gains are not spent back in the epilogue | bottleneck: Epilogue/export LSU and shared-memory round-trip overhead after the feed path has already been partially improved.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
