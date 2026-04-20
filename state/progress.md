# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `436e9ff0e79447691264b4a10ba8a0e499128da7`
- plateau counter: `42`
- round loop: `round 17/17`
- rounds remaining: `1`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 17/17.`

## Latest measured custom run

- run id: `20260420_164223_bf16_gemm_v1_436e9ff`
- run dir: `runs/20260420_164223_bf16_gemm_v1_436e9ff`
- correctness: `PASS`
- median runtime: `25.624064 ms`
- TFLOP/s: `28.372525 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_164308`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 17/17 diagnosis for run 20260420_164223_bf16_gemm_v1_436e9ff. Human-review mapping for this round: there is still no new explicit external idea family queued in state/human_review.md, so the ranking is driven entirely by the measured evidence accumulated inside this loop. The full A-then-B prefetch retime improved the narrower refill-only retime but still missed the accepted export base, which leaves exactly one prefetch permutation untested: keep the initial primes retimed while restoring the future refill to B-then-A. That hybrid permutation is now the only live primary family. The seam family is kept secondary only at its known 6144 local best, because 5888 already regressed. The broad 64x384 control stays tertiary for auditability because the repo has sweep ancestry for it, but the current-loop evidence already says to keep that family effectively closed unless every narrower option stalls.`
- dir_01: Keep The Initial Prime Retime But Restore The Future Refill To B-Then-A | bottleneck: Copy-pipeline handoff balance between long-scoreboard relief from the retimed initial primes and barrier pressure from the future-tile refill ordering in the PTX hot-band microkernel.
- dir_02: Restore The 6144 Seam As The Best Bounded Launch-Split Fallback | bottleneck: Boundary cost between the PTX hot-band kernel and the peeled 384-row row-band path, especially whether the fixed split point is leaving a small but repeatable launch handoff penalty.
- dir_03: Keep The Broad 64x384 Fixed-Main Control Only As A Tertiary Close-Out Control | bottleneck: Broader hot-band path selection and arithmetic-intensity tradeoff rather than PTX microkernel copy-order tuning.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
