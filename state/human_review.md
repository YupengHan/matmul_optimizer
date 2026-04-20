# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 5/17` with `13` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_155518`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5/17 diagnosis for run 20260420_155247_bf16_gemm_v1_10d32cf. Human-review mapping for this round: reject broad retile/default-promotion reopening and reject the immediate PTX prefetch-handoff family for now, because round 4 cut long-scoreboard to 5.83 but still regressed by +0.47713566 ms versus the accepted base, with barrier rising to 6.63 and no throughput gain. Also keep deeper export flattening closed after round 3. No new explicit human idea family is queued in state/human_review.md, so this round carries forward the surviving narrow idea families only: accept PTX B-shared skew as the primary next move, defer grouped-row/orchestration retuning as the main alternate, and keep only a minimal export cleanup as the low-risk reserve. The older main-tile sweep data is noted but not reopened this round because tonight's loop is staying on the accepted PTX baseline rather than broad branch changes.`
- dir_01: Tune PTX Hot-Band B-Shared Skew On The Accepted Export Base | bottleneck: Shared-memory B-fragment layout friction and address-generation overhead in the PTX hot-band path.
- dir_02: Retighten PTX Hot-Band Grouping / Orchestration Window | bottleneck: Hot-band CTA grouping and orchestration overhead around the PTX grouped-row mapping.
- dir_03: Apply Only A Minimal PTX Export Address Cleanup | bottleneck: Residual address-generation and store-helper overhead in the surviving PTX export path.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
