# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `13caa861e2dbca1a073e2998007fb1569bda03c9`
- plateau counter: `17`
- round loop: `round 2/30`
- rounds remaining: `29`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 2/30.`

## Latest measured custom run

- run id: `20260419_215456_bf16_gemm_v1_13caa86`
- run dir: `runs/20260419_215456_bf16_gemm_v1_13caa86`
- correctness: `PASS`
- median runtime: `30.618112 ms`
- TFLOP/s: `23.744751 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_215602`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2/30 starts from a recovered and credible exploratory anchor again. Restoring the round-8 streaming-B branch recovered runtime to 30.618112 ms and restored the better feed-side profile: tensor active back up to about 38.56, barrier stall back down to about 6.56, short scoreboard about 6.72, `mio_throttle` about 0.33, and registers back to the pre-producer level. That confirms the loop should keep working from this branch rather than keep spending rounds on resets. The shared-permutation and producer-only staging variants are already known negatives, so the next best move is the next remaining high-ceiling step on top of the streaming-B consumer path: a one-fragment Ps2r lookahead. Dir_02 keeps the stronger global baseline option (`b13027c`) in reserve if this branch stalls again. Dir_03 covers the next non-feed family on the same branch by trimming the export path.`
- dir_01: Human idea Ps2r: one-fragment shared-to-register lookahead on the restored streaming-B branch | bottleneck: Residual shared-to-register feed latency inside the hot-band 64x64 micro-tile after the streaming consumer cleanup.
- dir_02: Reset to the best measured custom commit `b13027c` and port future experiments from there | bottleneck: Not an immediate micro-bottleneck attack; this is a better global baseline reset for later rounds.
- dir_03: Trim the hot-band export path on top of the restored streaming-B branch | bottleneck: Epilogue/export LSU and shared-memory round-trip overhead after the feed path has already been partially improved.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
