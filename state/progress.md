# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `b8a113b50abd16e7da505f5c59a1ea8be4abc749`
- plateau counter: `19`
- round loop: `round 32/100`
- rounds remaining: `69`
- notes: `Node C build succeeded for round 32/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_013804_bf16_gemm_v1_b8a113b`
- run dir: `runs/20260421_013804_bf16_gemm_v1_b8a113b`
- correctness: `PASS`
- median runtime: `24.168880 ms`
- TFLOP/s: `30.080808 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_013852`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 32 starts from a recovered clean base, so the ranking can go back to fully aggressive directions instead of spending a slot on recovery. The key evidence from the last three rounds is now coherent: the accepted PTX anchor remains around 24.17 ms at 200 registers and about 16.6% active warps; the PTX launch-bounds probe proved that lower-register 3-CTA residency can move the machine state but suffered a barrier blowup; the x32 follow-on proved that barrier amortization cannot come from doubling shared memory to 43 KB. The next bounded aggressive probe should therefore test the same occupancy thesis on the correctness-proven non-PTX 128x128 sibling before reopening broader or more manual branches.`
- dir_01: Force 3-CTA Residency On The Non-PTX 128x128 Sibling | bottleneck: Register-limited occupancy and latency hiding on the non-PTX 128x128 sibling surface.
- dir_02: Trim Microkernel Barriers Without Reintroducing Shared-Memory Blowup | bottleneck: Barrier cadence inside the single-K 128x128 PTX microkernel while preserving the small shared-memory footprint.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and synchronization strategy on the 256x128 hot-band path, plus correctness-sensitive writer ownership.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
