# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 62/100` with `39` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_090253`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Anchored to run 20260420_090210_bf16_gemm_v1_06ebe93 at 25.634208 ms. Rejected this round: grouped_rows=16, warmup-order reopen, K32 cadence, extra-live B lookahead, unroll-1 base, CTA-level B repack, broad shared-memory rewrites, and consumer-order variants that replace the accepted right-left sweep as the active base.`
- dir_01: restore accepted base, then narrow locality window | bottleneck: Hot-band consumer-path locality and reuse window width on the accepted PTX sweep / handoff path.
- dir_02: accepted base, then narrow overlap recovery | bottleneck: Refill-order overlap around the one-sync handoff and staged consumer refill path.
- dir_03: final consumer-order closure | bottleneck: Residual consumer-order inefficiency in the hot-band PTX consumer path rather than grouping or refill layout.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
