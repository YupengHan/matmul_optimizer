# Progress

## Objective

Beat cuBLAS and drive the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1` to `<= 18.000 ms`.
- target runtime: `<= 18.000 ms`
- comparison target: `cuBLAS`
- rebootstrap source: `20260420_235922_bf16_gemm_v1_489574e`, commit `489574ed5013268dbb79c634450d9a60155a294a`, historical runtime `24.164272 ms`

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `afe26c16b7d2d62c7e91cb7725ccc9f7bbba0d01`
- plateau counter: `10`
- round loop: `round 6/10`
- rounds remaining: `5`
- notes: `Node C build succeeded for round 6/10. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_154110_bf16_gemm_v1_afe26c16`
- run dir: `runs/20260421_154110_bf16_gemm_v1_afe26c16`
- correctness: `PASS`
- median runtime: `30.168575 ms`
- TFLOP/s: `24.098567 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_154619`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human guidance review for round 6: the 256x128 / 64x64 idea family remains strategically relevant, but the latest clean-loop evidence says it should not be the next code edit. The round-4 256x128 pivot and round-5 compact transplant both left the branch in the same losing machine state, while the cuBLASLt reference makes the ceiling clearer: this workload is not missing raw active-warps so much as it is missing a low-friction synchronization and handoff regime. That is why dir_01 ranks first even though it steps away from the currently running 256x128 surface. The queue still preserves one bounded occupancy probe on the accepted non-PTX 128x128 sibling and one deferred high-ceiling 256x128 branch so the search does not collapse back into a single-family local minimum.`
- dir_01: Trim PTX Wait/Sync Handoff On The 128x128 Anchor | bottleneck: Barrier cadence and export/control handoff inside the single-K 128x128 PTX microkernel, especially the seam between finishing a tile, releasing the stage with __syncthreads(), and refilling the reused buffer.
- dir_02: Force 3-CTA Residency On The Non-PTX 128x128 Sibling | bottleneck: Register-limited occupancy and latency hiding on the accepted non-PTX 128x128 hot-band surface.
- dir_03: Reopen The 256x128 Half-Panel Register-Reuse Branch Later | bottleneck: Register reuse, B-fragment lifetime, and writer-ownership constraints inside the 256x128 hot-band pivot.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` of CUTLASS runtime (faster)
- cuBLAS median runtime: `22.000000 ms`
- current best custom gap vs cuBLAS: `2.164272 ms`, `1.098376x` of cuBLAS runtime (slower)
