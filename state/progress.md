# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `8b1af08daa22015817d74711dfdc12ec910d69a6`
- plateau counter: `88`
- round loop: `single-run`
- rounds remaining: `0`
- notes: `Node C build succeeded. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_084952_bf16_gemm_v1_8b1af08`
- run dir: `runs/20260421_084952_bf16_gemm_v1_8b1af08`
- correctness: `PASS`
- median runtime: `24.427104 ms`
- TFLOP/s: `29.762817 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_093739`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `The current kernel already matches the best historical PTX grouping surface at the source level, so this diagnosis avoids another replay cycle and focuses on real low-risk control-path tightening in the active 128x128 hot-band kernels.`
- dir_01: Hoist 128x128 Hot-Band Shared Offsets Out Of The Steady-State Loop | bottleneck: Warp-local shared-pointer arithmetic and loop-carried control overhead in the 128x128 hot-band steady state are stealing issue slots from tensor work.
- dir_02: Trim PTX 64x64 Export Address Math In The Hot-Band Epilogue | bottleneck: PTX export-side address generation in the 64x64 writer is adding integer/control overhead after the MMA loop.
- dir_03: Retime The 128x128 PTX Wait-Group And Consumer Barrier Handoff | bottleneck: The PTX 128x128 steady state may be overserializing cp.async wait-group completion and CTA-wide consumer handoff.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
