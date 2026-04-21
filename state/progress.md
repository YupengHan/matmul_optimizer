# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `894a38d5136472c4d63ae862d55459e4f8b35374`
- plateau counter: `24`
- round loop: `round 37/100`
- rounds remaining: `64`
- notes: `Node C build succeeded for round 37/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_075335_bf16_gemm_v1_894a38d`
- run dir: `runs/20260421_075335_bf16_gemm_v1_894a38d`
- correctness: `PASS`
- median runtime: `24.191999 ms`
- TFLOP/s: `30.052060 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_075421`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 37 explicitly chooses exploration over reflex recovery. The latest PTX control-path cleanup did not win, but it moved barrier and long-scoreboard in the right direction while staying within 0.02 ms of the restored base. That is exactly the kind of partial signal that justifies one more tightly bounded scheduler-seam retime before the loop falls back to restore or jumps to the broader 256x128 family.`
- dir_01: Steady-state Barrier / Handoff Retime | bottleneck: Residual wait-group and barrier cadence in the PTX hot-band steady-state loop, especially the seam between finishing the current MMA stage and refilling the reused stage buffer for the future tile.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Known register-limited plateau on the accepted PTX hot-band surface, used here as a clean recovery anchor if the scheduler-seam follow-up loses signal.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and synchronization strategy on the 256x128 hot-band path, plus correctness-sensitive writer ownership.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
