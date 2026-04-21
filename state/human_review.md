# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 2/10` with `9` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_142317_round02_5ea07e35`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2 should branch from the accepted base run 20260421_133418_bf16_gemm_v1_c859cd06, not from the round-1 regressed staged-kernel head. The top priority is to reduce time spent in the 128x128 hotspot rather than add more K-stage depth there.`
- dir_01: Restore The Accepted Base And Expand The 64x384 Row Band | bottleneck: too much of the fixed hot band is assigned to the 128x128 PTX hotspot instead of the stronger 64x384 family
- dir_02: Retune PTX Hot-Band Grouped-Row Traversal | bottleneck: launch-order and cache/locality inefficiency inside the accepted PTX hot-band traversal
- dir_03: Swap To The Single-K 128x128 Non-Microkernel Sibling | bottleneck: microkernel-specific accumulate/store scheduling inside the accepted 128x128 hot-band path

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
