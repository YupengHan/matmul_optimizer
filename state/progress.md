# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `06eedc6cae82b3b30f2ac78be257751b6684432a`
- plateau counter: `18`
- round loop: `round 3/30`
- rounds remaining: `28`
- notes: `Node C build succeeded for round 3/30. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_215841_bf16_gemm_v1_06eedc6`
- run dir: `runs/20260419_215841_bf16_gemm_v1_06eedc6`
- correctness: `PASS`
- median runtime: `30.592960 ms`
- TFLOP/s: `23.764272 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_215936`
- recommended direction: `dir_01`
- approved direction: `dir_02`
- diagnosis notes: `Round 3/30 starts from a branch that is directionally healthy but still fundamentally stuck on the register wall. The one-fragment B-side Ps2r lookahead built cleanly, preserved correctness, and improved runtime from 30.618112 ms to 30.592960 ms, but the gain is only about 0.025 ms and the headline profile barely moved: tensor active is still about 38.57%, active warps about 16.76%, `mio_throttle` is already low at about 0.33, short scoreboard remains about 6.74, and the hot-band kernel still uses about 167 registers per thread with `launch__occupancy_limit_registers = 1`. That means the loop has probably extracted most of the cheap B-feed cleanup available without changing the live working set. Recommended direction dir_01 therefore shifts to the user-provided register-reuse / phased-tiling family: keep the accepted 256x128 CTA and 64x64 warp geometry, but split the warp-local output columns into two mirrored 64x32 accumulator panels so the kernel can test whether reduced live accumulator footprint buys back occupancy and tensor activity. Dir_02 keeps the Ps2r family alive on the A side if the panelization looks too invasive, and dir_03 records the user-provided L2 traversal clue as a lower-priority structural experiment once the occupancy-side opportunities are exhausted.`
- dir_01: Human idea register reuse: phase the 64x64 hot-band warp tile into two 64x32 accumulator panels | bottleneck: Register-limited occupancy and warp-level live-fragment pressure in the hot-band PTX microkernel.
- dir_02: Human idea Ps2r: preload the next A row-pair while the current row-pair consumes the mirrored B stream | bottleneck: Residual shared-to-register latency on the A side inside the hot-band row-pair sweep after the B side has already been partially overlapped.
- dir_03: Human idea L2 cache clue: try a grouped CTA traversal for the 256x128 hot band | bottleneck: Potential L2 locality loss from the default CTA traversal over the fixed hot-band grid.

## Active implementation direction

- direction id: `dir_02`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
