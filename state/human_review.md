# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 2/5` with `4` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_102638`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2/5 diagnosis prepared from the current best custom run 20260419_102608_bf16_gemm_v1_2872f92 at 35.677088 ms. Recent history is applied explicitly: broad B-feed rewrites and phased live-set rewrites regressed, peeled hot-kernel specialization plus trimmed export won, and deeper single-skew overlap improved again. Ranking therefore keeps the peeled 64x384 hot kernel as the base, prioritizes barrier/stage-recycle cleanup next, then further export trimming, and leaves tail specialization as the lower-upside third option.`
- dir_01: Reduce stage-recycle barriers in the peeled 64x384 hot loop | bottleneck: CTA-wide synchronization and stage handoff overhead inside the peeled 64x384 steady-state loop.
- dir_02: Trim the peeled hot-kernel export path beyond the current quad writeback | bottleneck: Epilogue-side shared export and LSU pressure after the peeled hot loop finishes MMA.
- dir_03: Peel and specialize the fixed 64x96 tail kernel to match the hot path | bottleneck: Residual tail overhead from using the generic 64x96 tensor-core kernel on a fixed-shape tail region.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
