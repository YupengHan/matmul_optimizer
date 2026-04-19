# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `awaiting_direction_selection_for_node_c`
- round loop: `round 2/5` with `4` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_131829`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `All three directions stay inside the 64x384 hot-band PTX microkernel branch. The 64x96 tail remains unchanged. Ranking is anchored on the current accepted PTX base 4ad2ee7: runtime improved materially over the WMMA base, mio dropped to 5.53, but the hot kernel now runs at 172 registers/thread with occupancy_limit_registers=1 and only 16.47 active warps. That makes occupancy and live-state recovery the main guardrail for round 2, while still pushing deeper into explicit PTX fragment/load/export control rather than reverting to generic WMMA tuning.`
- dir_01: Explicit ldmatrix PTX microkernel with smaller hot-band live set | bottleneck: Register footprint and live-fragment residency inside the current PTX hot-band compute body are limiting occupancy and latency hiding; explicit fragment control is needed to lower that footprint without abandoning the PTX branch.
- dir_02: Wrapper-level PTX accumulator phasing before full ldmatrix rewrite | bottleneck: The dominant cost is accumulator live-set size, not the cp.async path and not the tail kernel, so reducing simultaneously resident PTX accumulator tiles should help occupancy first.
- dir_03: Register-first PTX export path after compute-body control | bottleneck: The hot-band export path is still consuming shared/LSU budget and can become the next limiter once mio has already been cut; taking control of export is the natural PTX-branch follow-on after compute-body control.

## Active direction

- selected direction: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`
