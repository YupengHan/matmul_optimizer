# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 3/10` with `8` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_145629_round03_5383596d`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3 should return to the accepted base run 20260421_133418_bf16_gemm_v1_c859cd06 before implementing any new direction. The 64x384 row-band expansion family is now explicitly deprioritized after the 47.291 ms regression.`
- dir_01: Restore The Accepted Base And Increase PTX Grouped-Row Depth | bottleneck: launch-order and B-tile reuse inefficiency inside the accepted PTX hot-band traversal
- dir_02: Restore The Accepted Base And Swap To The Single-K 128x128 Sibling | bottleneck: microkernel-specific accumulate ordering is contributing to scoreboard overhead on the accepted hot-band split
- dir_03: Restore The Accepted Base And Tighten PTX Launch Bounds | bottleneck: register pressure and low CTA residency on the accepted PTX hot-band path

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
