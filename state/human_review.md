# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 10/50` with `41` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_190757`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 10/50 diagnosis for regressed run 20260420_190726_bf16_gemm_v1_cc89c17 while the implementation surface has already been restored to the accepted 1181247 base. Human-review reflection is explicit here: state/human_review.md contains queue state only and no new user-provided idea bullets, so this round makes the family mapping directly from the measured evidence. Rejected for this round: promoting the peeled single-stage residual family as the new default, because cc89c17 regressed to 25.152928 ms despite improving the peeled kernel in the NCU capture. Accepted as the primary family: tail-only cleanup on the restored 1181247 surface, because the 64x96 tail remains the highest-stall bounded outlier in the latest measured profile and does not require reopening the regressed default family. Deferred but still valid: a gated re-test of the peeled single-stage export family and the alternate PTX 128x128 hot-band control branch. Also rejected for ranking this round: the stale broad fixed-main autotune sweep from round 18 and the older 256x128 auxiliary branch, because neither outranks the restored-base tail cleanup after the cc89c17 regression.`
- dir_01: Trim The Fixed 64x96 Tail On The Restored 1181247 Base | bottleneck: Generic 64x96 tail staging and epilogue synchronization overhead on the restored fixed split.
- dir_02: Reintroduce The Peeled Single-Stage Export Only Behind An Explicit Gate | bottleneck: Residual 64x384 epilogue export lifetime and cross-kernel interaction at the hot-band to peeled handoff, not the dominant hot-band kernel itself.
- dir_03: Reopen The PTX 128x128 Hot-Band Branch As The Alternate Recovery Family | bottleneck: Dominant 128x128 hot-band control flow and export-scratch behavior rather than the residual or tail kernels.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
