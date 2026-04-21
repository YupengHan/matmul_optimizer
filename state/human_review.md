# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 25/100` with `76` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_010737`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 25 intentionally overrides the frontier's current micro-family ordering. The plateaued PTX families are now treated as low-value noise-chasing, while the auxiliary 256x128 family is promoted as the best remaining structural probe after the half-panel closeout.`
- dir_01: Reopen The Auxiliary 256x128 Hot-Band Schedule As The Next Structural Probe | bottleneck: Hot-band CTA geometry, control amortization, and latency hiding on the wide 256x128 schedule family, not another PTX-local barrier or scoreboard seam on the already plateaued 128x128 winner surface.
- dir_02: Restore The Grouped-Row Non-PTX 128x128 Sibling Surface | bottleneck: PTX-microkernel-specific control and export coupling on the current winner surface, while preserving the same broad 128x128 footprint and grouped-row locality.
- dir_03: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: No new bottleneck is being attacked here; this is the exact baseline recovery path back to the best measured correct surface.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
