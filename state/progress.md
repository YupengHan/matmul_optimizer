# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `1128e91796b4c957cc60438bdbf761cd725cb821`
- plateau counter: `9`
- round loop: `round 4/10`
- rounds remaining: `7`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 4/10.`

## Latest measured custom run

- run id: `20260419_205932_bf16_gemm_v1_1128e91`
- run dir: `runs/20260419_205932_bf16_gemm_v1_1128e91`
- correctness: `FAIL`
- median runtime: `31.486465 ms`
- TFLOP/s: `23.089903 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_210044`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4 human-idea audit against the latest evidence: Tiling is still accepted historically, but its implication changes this round because the live half-panel implementation is now an unstable branch rather than a promising near-finish; Coalescing Access, Data Reuse, and Async Copy remain accepted as baseline properties of both the unstable half-panel branch and the accepted base; Bank Conflict becomes the primary accepted family for the next correct-branch work because the user explicitly asked that any renewed B-feed experiment stay warp-local and avoid CTA repack; L2 Cache remains deferred because neither the latest incorrect run nor the accepted base is L2-bound; Register Reuse is demoted for this round because the half-panel branch stayed incorrect and unstable through round 3 despite preserving the 93-reg / 2-block signal; Pg2s, Ps2r, and Stage remain accepted as future correct-branch follow-ups, not as justification for another blind half-panel repair. The decisive new evidence is local rerun instability after round 3: the same correctness case still changes max-error index and value across reruns, while mean_abs_err stays around 0.033 and the measured run regressed to 31.486 ms. That is enough to stop treating the current half-panel implementation as one round away. Recommended direction dir_01 therefore resets the loop to the last correct accepted base first. With six rounds left after that reset, the loop can spend its remaining budget on correct-branch optimization again instead of continuing to debug an unstable branch.`
- dir_01: Human idea 5 fallback reset: restore the last correct accepted base before spending more rounds on the hot branch | bottleneck: The immediate bottleneck is workflow risk, not another micro-metric: the current half-panel branch is still an incorrect and unstable implementation. Restoring the accepted base removes that blocker so the next rounds can optimize a correct kernel again.
- dir_02: Human idea 7 last-chance sparse-error repair: keep the half-panel branch alive for one more ownership-focused round | bottleneck: Residual sparse ownership/coverage bug in the half-panel path rather than feed throughput.
- dir_03: Human idea 5 bank-conflict follow-through on the correct branch: restore the accepted base and immediately retune the warp-local B consumer path | bottleneck: Shared/L1/B-operand delivery behavior on the restored correct branch rather than occupancy.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
