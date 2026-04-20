# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `5dd9f0d02883a3b1debb9d3933a489c44bc0330d`
- plateau counter: `0`
- round loop: `round 5/30`
- rounds remaining: `26`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 5/30.`

## Latest measured custom run

- run id: `20260419_221014_bf16_gemm_v1_5dd9f0d`
- run dir: `runs/20260419_221014_bf16_gemm_v1_5dd9f0d`
- correctness: `PASS`
- median runtime: `29.432832 ms`
- TFLOP/s: `24.700968 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_221100`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5/30 starts from the new best custom branch. Restoring the last correctness-valid hot-band surface unexpectedly measured at 29.432832 ms with correctness restored, shrinking the CUTLASS gap to about 3.51 ms. The detailed profile, however, still does not show an obvious new single micro-bottleneck: the hot-band kernel remains around 40.99 us, registers stay at about 167/thread, tensor active stays around 38.63%, active warps around 16.67%, and both DRAM and L2 throughput remain modest. Because the branch is now both valid and relatively strong, this is a good point to spend one round on the user-provided L2-launch-order clue instead of forcing another fragile feed-side rewrite. Recommended direction dir_01 therefore tries a grouped CTA traversal for the fixed hot-band grid. Dir_02 keeps the next bank-conflict / consumer-delivery human idea in reserve without violating the no-extra-shared rule, and dir_03 captures the remaining coalescing / async-copy ownership experiment once the traversal clue has been tested.`
- dir_01: Human idea L2 cache clue: grouped CTA traversal for the fixed hot-band grid | bottleneck: Potential L2 locality loss from the default hot-band CTA traversal over the 60x25 grid.
- dir_02: Human idea bank conflict: try a lighter warp-local B consumer remap with no shared-footprint growth | bottleneck: Residual B-side shared-to-register delivery inefficiency and bank behavior inside the 64x64 hot-band PTX consumer path.
- dir_03: Human idea coalescing + async copy: retune cp.async ownership so each warp stages contiguous stripes | bottleneck: Global-to-shared staging instruction overhead and issue regularity rather than raw DRAM bandwidth.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.514943 ms`, `1.135618x` slower than CUTLASS
