# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 61/100` with `40` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_090007`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Anchored to the latest measured run 20260420_085928_bf16_gemm_v1_9ee9b48 at 25.821696 ms. Keep the accepted grouped_rows=8 base, reversed PTX row-pair traversal, right-left PTX column sweep, and one-sync wait_group_0 handoff as the primary baseline; keep split sweep, full mirrored sweep, grouped_rows=16, warmup-order reopen, K32 cadence, extra-live B lookahead, unroll-1 base, CTA-level B repack, and broad shared-memory rewrites closed for this round.`
- dir_01: Restore accepted base, then retime refill issue order | bottleneck: Refill issue ordering after the accepted one-sync handoff, not the consumer sweep order itself.
- dir_02: Minimal overlap recovery behind the one-sync handoff | bottleneck: Residual overlap loss in the steady-state handoff window after the accepted consumer path has already drained.
- dir_03: Very local consumer-order closure only | bottleneck: Residual consumer-side locality loss in the hot-band PTX sweep, limited to a small ordering closure.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
