# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 59/100` with `42` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_085345`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Anchored to run 20260420_084915_bf16_gemm_v1_4e5579e at 24.570881 ms. Accepted themes this round were Register Reuse, Ps2r, and Bank Conflict. Rejected this round: grouped_rows=16, warmup-order reopen, K32 cadence, extra-live B lookahead, unroll-1 base, CTA-level B repack, and broad shared-memory rewrites.`
- dir_01: PTX hot-band consumer-order refinement | bottleneck: Long scoreboard latency in the PTX hot-band consumer path, not the barrier or shared-memory handoff itself.
- dir_02: Recover overlap behind the one-sync wait_group_0 handoff | bottleneck: Residual overlap loss after the single wait_group_0 + __syncthreads() handoff, now exposed mainly as long scoreboard.
- dir_03: Limited locality closure with grouped_rows=8 only | bottleneck: Minor locality loss in the grouped_rows=8 dispatch order, not a structural tile-size problem.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
