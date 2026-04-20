# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `0c0ee9b007ed96d28f6b3c89a113cc8d68fe88c6`
- plateau counter: `12`
- round loop: `round 13/50`
- rounds remaining: `38`
- notes: `Node C build succeeded for round 13/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_232036_bf16_gemm_v1_0c0ee9b`
- run dir: `runs/20260419_232036_bf16_gemm_v1_0c0ee9b`
- correctness: `FAIL`
- median runtime: `30.695935 ms`
- TFLOP/s: `23.684550 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_232121`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 13/50 shifts away from the stage family because the 3-stage hot-band branch only moved the dominant kernel from about 41.11 ms to 41.18 ms while breaking correctness and driving barrier stalls much higher. The recommended next family is the user's consumer-side B feed idea under strict constraints: no extra shared footprint, no extra CTA barriers, and no CTA-level repack.`
- dir_01: Restore the accepted-correct hot-band surface and apply a warp-local B XOR/interleaved consumer swizzle with zero extra shared footprint | bottleneck: Shared-memory bank behavior and warp-local B operand delivery in the hot-band PTX consumer path.
- dir_02: Restore the accepted surface and start an explicit ldmatrix/mma.sync hot-band microkernel branch | bottleneck: Tensor Core under-utilization caused by the current WMMA-based fragment load and issue model rather than tile shape alone.
- dir_03: Restore the accepted-correct implementation surface before the next experiment | bottleneck: Not a bottleneck attack; this is the reset path that keeps later rounds interpretable.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
