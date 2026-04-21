# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `2e4dd246f55b505bd095c42b62c56dc497c8fde1`
- plateau counter: `0`
- round loop: `round 3/50`
- rounds remaining: `48`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 3/50.`

## Latest measured custom run

- run id: `20260420_180146_bf16_gemm_v1_2e4dd24`
- run dir: `runs/20260420_180146_bf16_gemm_v1_2e4dd24`
- correctness: `PASS`
- median runtime: `24.444416 ms`
- TFLOP/s: `29.741738 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_180213`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3/50 diagnosis anchored to run `20260420_180146_bf16_gemm_v1_2e4dd24`, which is now the accepted base and the first custom result faster than the local CUTLASS baseline. The ranking therefore stays on the winning grouped-rows-4 PTX surface instead of reopening broad structural pivots. Accepted as the primary family: steady-state hot-band handoff / consume retiming, because the dominant kernel still carries 7.43% long scoreboard and 5.61% barrier stall with tensor active only 48.16%. Accepted as the secondary materially different family: register/export lifetime trimming, because the win did not move the 200-register occupancy wall. Deferred to tertiary: a bounded seam repivot, because the peeled+tail kernels are still barrier-heavy but prior seam evidence remains weaker than the hot-band families. Rejected for this round: reopening K32 or broad fixed-main control families, because the latest measured evidence already beat CUTLASS on the current surface and those broader pivots are not the best next tradeoff.`
- dir_01: Retune The Hot-Band Steady-State Handoff On The New Grouped-Rows-4 Base | bottleneck: Steady-state cp.async handoff latency and fragment-consume ordering inside the active 128x128 PTX hot-band loop, which is still leaving tensor issue on the table after the grouped-row locality fix.
- dir_02: Trim PTX Accumulator And Export Live Range On The New Best Surface | bottleneck: Register pressure and export-side live-state lifetime in the PTX hot-band microkernel, which is capping occupancy before the kernel reaches a memory-throughput limit.
- dir_03: Probe A Bounded Hot-Band Seam Repivot Around The Grouped-Rows-4 Winner | bottleneck: Boundary placement between the 128x128 PTX hot-band kernel and the peeled 64x384 row-band launch, especially whether the fixed 6400-row split is leaving avoidable barrier-heavy work in the secondary kernels.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.473473 ms`, `0.943148x` slower than CUTLASS
