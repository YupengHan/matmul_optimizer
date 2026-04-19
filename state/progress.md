# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `ea27d5a906ceb46b0a4ec429d6d53f4a457620d6`
- plateau counter: `0`
- round loop: `round 19/20`
- rounds remaining: `2`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 19/20.`

## Latest measured custom run

- run id: `20260419_013130_bf16_gemm_v1_ea27d5a`
- run dir: `runs/20260419_013130_bf16_gemm_v1_ea27d5a`
- correctness: `PASS`
- median runtime: `38.473728 ms`
- TFLOP/s: `18.896516 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_013222`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 19/20 diagnosis uses many human-in-loop inspirations explicitly. The round-18 autotune sweep is treated as strong evidence that 64x384 main over 7680 columns plus the 64x96 tail is the right macro split on this machine, so the ranked directions focus on the dominant TensorCoreTileConfig<12> hot kernel rather than the ~0.93 time-unit tail kernel. Raw ncu_details.csv was used to go beyond the shallow headline summary: main-kernel 64x384 runs with 126 registers/thread, 38.4 KB shared/block, 77.865532% LSU instruction issue, 48.590499% LSU wavefront activity, 30.726069% DRAM cycles active, 31.42% MIO throttle, and only 32.130750% tensor active. The recommendation is therefore to shift work more intelligently toward Tensor Cores by reducing shared/L1/LSU overhead inside the proven 64x384 path, not by blindly widening tiles again.`
- dir_01: Keep 64x384, but rework the hot-kernel shared/L1 feed path | bottleneck: Shared-memory and LSU feed pressure in the 64x384 hot band is throttling Tensor Core issue; the problem is now on-chip instruction mix and staging efficiency, not the macro tile width.
- dir_02: Trim hot-kernel epilogue and other non-tensor writeback work | bottleneck: Instruction mix and epilogue-side LSU/synchronization work are diluting Tensor Core utilization inside the main kernel.
- dir_03: Keep the 64x384 macro tile, but shrink per-warp fragment footprint | bottleneck: Register-limited occupancy and low ready-warp count inside the 64x384 hot kernel are preventing the widened main tile from fully converting into higher tensor activity.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `12.555840 ms`, `1.484447x` slower than CUTLASS
