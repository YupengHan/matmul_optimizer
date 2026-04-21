# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `e1c12b7e611db6887f307c378b80accb49501bca`
- plateau counter: `1`
- round loop: `round 4/50`
- rounds remaining: `47`
- notes: `Node C build succeeded for round 4/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_181354_bf16_gemm_v1_e1c12b7`
- run dir: `runs/20260420_181354_bf16_gemm_v1_e1c12b7`
- correctness: `PASS`
- median runtime: `25.515008 ms`
- TFLOP/s: `28.493796 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_181421`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4/50 diagnosis anchored to run `20260420_181354_bf16_gemm_v1_e1c12b7`, with the implementation surface already restored to the accepted best measured commit `2e4dd246f55b505bd095c42b62c56dc497c8fde1`. The latest run is strong negative evidence against continuing the grouped-rows-4 handoff-retime family: the end-to-end median regressed by 1.070592 ms, but the dominant hot-band kernel barely moved versus the accepted base and kept the same 200-register / register-limited occupancy wall. That closes handoff-retime as the primary family for the next round. The ranking therefore pivots to the surviving materially different options on the restored winner: first register/export lifetime trimming because the occupancy wall remains completely open; second the bounded 6144 seam because the peeled and tail kernels are still barrier-heavy but the family is already known to be lower-upside than the current base; third the broad 64x384 fixed-main audit branch because the autotune ancestry still exists, but broad control reopening is much less credible now that the PTX winner already beats CUTLASS.`
- dir_01: Trim PTX Accumulator And Export Live Range On The Restored Grouped-Rows-4 Base | bottleneck: Register pressure and export-side live-state lifetime in the PTX hot-band microkernel, which is still capping occupancy and latency hiding on the restored best surface.
- dir_02: Restore The 6144 Hot-Band/Peeled Seam As The Best Launch-Split Fallback | bottleneck: Boundary cost between the dominant 128x128 PTX hot-band launch and the peeled 64x384 follow-on path, especially whether the fixed 6400-row split leaves avoidable barrier-heavy work in the secondary kernels.
- dir_03: Keep The Broad Fixed-Main 64x384 Control Only As An Audit Branch | bottleneck: Broader dispatch-path choice and arithmetic-intensity tradeoff across the fixed-shape hot band, not the inner PTX hot-band microkernel itself.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.473473 ms`, `0.943148x` slower than CUTLASS
