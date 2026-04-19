# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `01d00409efc03fdf555fef3ea7cc4efd403a720a`
- plateau counter: `0`
- round loop: `round 11/20`
- rounds remaining: `10`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 11/20.`

## Latest measured custom run

- run id: `20260418_235548_bf16_gemm_v1_01d0040`
- run dir: `runs/20260418_235548_bf16_gemm_v1_01d0040`
- correctness: `PASS`
- median runtime: `43.697664 ms`
- TFLOP/s: `16.637489 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_235617`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Rounds 10-14 are intentionally biased toward more aggressive experiments. This round is chasing the new bottleneck from a first-principles instruction-mix perspective: the 43.70 ms round-10 win increased math per barrier and dropped barrier stalls, but the hot 64x128 main kernel is now the clear frontier with MIO throttle at 41.76%, register-limited occupancy at 4 blocks/SM, and L1TEX/LSU request pressure near 82.8%. The three directions therefore favor structural feed and epilogue changes over small parameter nudges.`
- dir_01: Main-kernel producer/consumer cp.async pipeline | bottleneck: Main-path MIO/LSU issue saturation in the 64x128 feed pipeline, with residual CTA-wide handoff cost as a secondary limiter.
- dir_02: Scratch-free or vectorized BF16 epilogue for the 64x128 main path | bottleneck: Epilogue-side MIO and shared-memory round-trip pressure layered on top of an already LSU-saturated main kernel.
- dir_03: Retile the hot main kernel to cut live B-fragment and accumulator pressure | bottleneck: Register-limited occupancy and per-K-step B-feed MIO pressure caused by the four-fragment 64x128 warp organization.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `17.779776 ms`, `1.686004x` slower than CUTLASS
