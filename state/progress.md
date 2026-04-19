# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `77f95870d9eaf181f0be8556393e50ed38d1dd72`
- plateau counter: `10`
- round loop: `round 1/5`
- rounds remaining: `5`
- notes: `Node C build succeeded for round 1/5. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_130737_bf16_gemm_v1_77f9587`
- run dir: `runs/20260419_130737_bf16_gemm_v1_77f9587`
- correctness: `PASS`
- median runtime: `36.671488 ms`
- TFLOP/s: `19.825196 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_130817`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- diagnosis notes: `This diagnosis intentionally keeps all three directions on the same human-directed 64x384 hot-band PTX microkernel branch. The 64x96 tail remains unchanged in every direction, and the round-18 sweep still anchors 64x384 as the right hot-band macro tile. Strong negative evidence from earlier warp specialization, producer straight-lining, and consumer-side B swizzle means the branch should not revert to generic WMMA cleanup or other old feed-path experiments; later rounds should refine the explicit PTX hot-band path instead.`
- dir_01: PTX hot-band microkernel branch with unchanged 64x96 tail | bottleneck: The dominant limiter is the WMMA hot-band control surface itself: it constrains fragment lifetime and instruction ordering, which keeps tensor issue diluted by feed/orchestration overhead even though the macro tile and tail split are already well chosen.
- dir_02: PTX phase 1 compute-core swap under current staging and tail split | bottleneck: Instruction selection and fragment scheduling inside the hot compute body, not the launch split and not the fixed 64x96 tail.
- dir_03: PTX register-first export and overlap-budget follow-through | bottleneck: The hot-band export path and c_shared round-trip still consume shared-memory and LSU budget that could otherwise support more overlap once the PTX branch owns accumulator residency.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `8.737343 ms`, `1.337116x` slower than CUTLASS
