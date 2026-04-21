# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 2/10` with `9` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_150910_round02_clean_7496aff2`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `This diagnosis continues the clean 10-round loop. The 8-row grouped setting is now treated as a measured negative result, so the next recommended clean round moves to the non-microkernel sibling.`
- dir_01: Swap To The Single-K 128x128 Non-Microkernel Sibling | bottleneck: microkernel-specific accumulate ordering is contributing to long-scoreboard stalls on the accepted hot-band split
- dir_02: Retune PTX Launch Bounds On The Clean Baseline | bottleneck: register pressure and low CTA residency on the accepted PTX hot-band path
- dir_03: Try A Shallower PTX Grouped-Row Setting | bottleneck: current grouped-row traversal may still be mismatched to A/B locality balance on the accepted PTX hot-band path

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
