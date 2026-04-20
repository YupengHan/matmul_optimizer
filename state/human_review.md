# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 54/100` with `47` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_082833`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `N/A`
- diagnosis notes: `Accepted this round: the B-first cp.async handoff family, constrained to the already-accepted grouped-row=8 + K16 + no-lookahead + single-scratch export base. Deferred: export/live-range trimming, because it is still plausible but secondary to the handoff retiming. Rejected: reopening the A-first warmup / B-first refill branch, because the latest experiment regressed and the evidence still points to steady-state handoff timing rather than warmup order.`
- dir_01: Retune the accepted B-first cp.async handoff inside the K16 hot band | bottleneck: Async-copy feed/issue retiming and stage handoff latency inside the active PTX hot-band microkernel.
- dir_02: Trim PTX export and accumulator live range on the accepted single-scratch surface | bottleneck: Register pressure and export-side synchronization / live-range overhead in the PTX hot-band epilogue.
- dir_03: Reopen the warmup A-first / refill B-first branch only as a closure probe | bottleneck: Warmup ordering is not the primary limiter; the current loss is in steady-state handoff timing on the accepted base.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
