# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 38/100` with `63` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_082719`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 38 uses restore-first ranking to recover the accepted PTX anchor before reopening the next PTX control-path retime or the structural 256x128 pivot.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Source drift away from the accepted PTX hot-band steady state, not DRAM saturation and not another immediate structural pivot.
- dir_02: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual cp.async wait-group timing and inner-loop control cadence in the PTX 128x128 hot-band microkernel after the restore anchor is back in place.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Structural latency hiding and register/shared-memory amortization on the hot band, not one more tiny PTX-local ordering tweak.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
