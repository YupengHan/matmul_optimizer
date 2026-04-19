# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `79cdb4341e0f3a30327d811f49424bb324cbbf43`
- plateau counter: `0`
- round loop: `round 17/20`
- rounds remaining: `4`
- notes: `Node C build succeeded for round 17/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_010405_bf16_gemm_v1_79cdb43`
- run dir: `runs/20260419_010405_bf16_gemm_v1_79cdb43`
- correctness: `PASS`
- median runtime: `42.564560 ms`
- TFLOP/s: `17.080393 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_010436`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `This diagnosis builds directly on the successful round-16 widened-main 64x160 + 64x96 result at 42.56455994 ms.`
- dir_01: 64x192 main + 64x128 middle + 64x96 tail fixed split | bottleneck: The main bottleneck should remain tensor-core under-utilization in the dominant hot band, with barrier and MIO throttle caused by too many medium-width CTAs rather than raw DRAM bandwidth.
- dir_02: 64x256 super-main over 7680 columns with minimal cleanup launches | bottleneck: The likely limiter shifts from launch granularity to occupancy and register/shared pressure: the super-main tile may improve tensor utilization only if its larger block does not push the kernel into a lower-latency-hiding regime.
- dir_03: Keep 64x160 main and collapse the fixed-shape cleanup path | bottleneck: The hot band remains limited by the same tensor/barrier/MIO behavior as round 16, but the target here is residual fixed-shape cleanup overhead from the separate 64x96 tail path rather than a new tile-level compute schedule.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `16.646671 ms`, `1.642285x` slower than CUTLASS
