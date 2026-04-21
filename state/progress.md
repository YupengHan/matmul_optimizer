# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `342b1c5e41fb67ca4f7d1bc26a811a491ec7c3cf`
- plateau counter: `93`
- round loop: `round 2/100`
- rounds remaining: `99`
- notes: `Node C build succeeded for round 2/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_110929_bf16_gemm_v1_342b1c5`
- run dir: `runs/20260421_110929_bf16_gemm_v1_342b1c5`
- correctness: `PASS`
- median runtime: `30.168576 ms`
- TFLOP/s: `24.098566 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_110945`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2 diagnosis prioritizes recovery after the 256x128 probe regressed badly while only partially solving the original register hotspot.`
- dir_01: Restore the accepted PTX hot-band anchor and discard the failed 256x128 probe | bottleneck: Recovery to the known PTX plateau before any further latency-hiding or barrier experiment is attempted
- dir_02: Recover the PTX baseline, then trim live control state before retrying geometry | bottleneck: occupancy_latency_hiding_issue on the accepted PTX hot-band path, with barrier as a secondary seam
- dir_03: If 256x128 is revisited, pivot from register shaving to barrier and short-scoreboard cleanup | bottleneck: synchronization_barrier_issue and short_scoreboard pressure inside the 256x128 pivot after the register budget has already been reduced

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
