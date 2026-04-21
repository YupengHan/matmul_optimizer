# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 40/100` with `61` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_082315`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 40 restores the accepted PTX anchor first, then keeps the 256x128 pivot and grouped-rows=8 consumer-ordering surfaces live for the post-checkpoint queue.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Source drift away from the accepted PTX hot-band steady state after a measured-loss reopen, not DRAM saturation and not an immediate need for another same-family micro-retime.
- dir_02: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Structural latency hiding and register/shared-memory amortization on the hot band, not another tiny PTX-local ordering tweak.
- dir_03: Restore Accepted Grouped-Rows-8 Hot-Band Consumer Ordering | bottleneck: Grouped-row traversal and consumer-order locality in the PTX hot-band path, not the already-closed wait/commit-window retime family.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
