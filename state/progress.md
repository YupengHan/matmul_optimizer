# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `a16425ea78ba002017dddae0549ba500472fb9e5`
- plateau counter: `21`
- round loop: `round 34/100`
- rounds remaining: `67`
- notes: `Node C build succeeded for round 34/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_014255_bf16_gemm_v1_a16425e`
- run dir: `runs/20260421_014255_bf16_gemm_v1_a16425e`
- correctness: `PASS`
- median runtime: `24.171008 ms`
- TFLOP/s: `30.078159 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_073952`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 34 starts from a cleanly restored PTX anchor rather than from a regressed live surface. That changes the diagnosis ranking: recovery is no longer the next action. The evidence from rounds 29 through 32 still matters, though, because both 128x128 launch-bounds probes showed the same causal shape: lower registers and higher active warps alone are not enough if synchronization cost spikes. That makes PTX-local barrier/control surgery the best next move on the restored anchor, with a bounded same-surface control-path exploit as the lower-risk fallback and the 256x128 low-register transplant still reserved as the high-ceiling, high-risk branch.`
- dir_01: Trim PTX Microkernel Barriers On The Restored 128x128 Anchor | bottleneck: Barrier cadence and PTX export/control handoff inside the single-K 128x128 PTX hot-band microkernel, now that recovery is complete and the failed residency probes isolated synchronization as the limiting tax on higher occupancy.
- dir_02: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual control-path overhead and live-range pressure inside the accepted PTX one-K 128x128 hot-band branch.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and synchronization strategy on the 256x128 hot-band path, plus correctness-sensitive writer ownership.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
