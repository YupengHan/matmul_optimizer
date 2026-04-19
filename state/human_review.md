# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 10/20` with `11` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_234449`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Using docs/heuristics.md explicitly, the current 64x96 kernel is no longer a simple DRAM-bound case; it is a mixed class-1 tensor under-utilization, class-3 shared/LSU feed pressure, and class-5 synchronization problem. Tensor active is 28.78%, warps active is already 82.91%, barrier stall is 29.48%, MIO throttle is 34.18%, LSU issue is 83.94%, and DRAM is only 47.58%, so rounds 10-14 are intentionally biased toward more aggressive experiments that materially change instruction mix rather than another small steady-state cleanup tweak, because the project is still far from the long-horizon ~20 ms target.`
- dir_01: Split the fixed shape into a 64x128 main kernel plus a 64x96 tail kernel | bottleneck: Barrier and fragment-feed overhead in the steady-state K loop; the current CTA already improved residency, so the next step is to amortize `cp.async`, `__syncthreads()`, and `wmma::load_matrix_sync` across more MMA before the next handoff.
- dir_02: Turn the lockstep cp.async loop into a warp-specialized producer-consumer pipeline | bottleneck: CTA-wide serialization of staging and compute work, plus MIO saturation from making every warp execute copy/setup work on every 16-wide K step.
- dir_03: Remove the `c_shared` round-trip and emit a register-first BF16 epilogue | bottleneck: Epilogue-side MIO and LSU pressure from the `c_shared` store-reread-convert-write sequence, which adds non-tensor instructions after the main MMA loop.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
