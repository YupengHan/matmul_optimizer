# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 6/17` with `12` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_160050`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 6/17 diagnosis for run 20260420_155914_bf16_gemm_v1_8297078. Human-review mapping for this round: keep broad retile/default-promotion, deeper export flattening, and the immediate prefetch-handoff family closed. Also close the specific expanded B-shared-skew implementation from round 5/17, because despite a 25.75615978 ms perf reading it failed correctness in all 3/3 cases with runner exit code 1, which is a harder rejection than a small runtime regression. No new explicit human idea family is queued in state/human_review.md, so this round carries forward only the surviving bounded families on the restored accepted base 20260420_154827_bf16_gemm_v1_7adfc4e at 25.50532818 ms: accept PTX grouping/orchestration retuning as the next primary move, defer a minimal export cleanup as the low-risk alternate, and keep the non-PTX 128x128 sibling only as a control path if the PTX-adjacent moves stall.`
- dir_01: Retighten PTX Hot-Band Grouping / Orchestration Window | bottleneck: Long-scoreboard and barrier cost caused by PTX hot-band grouping and grouped-row orchestration.
- dir_02: Apply Only A Minimal PTX Export Address Cleanup | bottleneck: Residual address-generation overhead in the surviving PTX export/store helper path.
- dir_03: Use The Non-PTX 128x128 Sibling As A Control | bottleneck: PTX-specific export/store and orchestration overhead versus the simpler non-PTX 128x128 sibling.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
