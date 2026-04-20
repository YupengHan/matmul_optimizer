# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 57/100` with `44` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_084408`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Anchored to measured run 20260420_084312_bf16_gemm_v1_57d08c3 at 24.713584 ms. Rejected this round: reopening warmup-order, K32 cadence, extra-live B lookahead, unroll-1 base, CTA-level B repack, and broad shared-memory rewrites.`
- dir_01: Hot-band L2 / grouped-row launch-order refinement | bottleneck: Improved L2 locality and reduced B-tile churn should trim long scoreboard pressure without reopening the already-accepted one-sync handoff base.
- dir_02: PTX hot-band consumer-order refinement | bottleneck: The warp consumer order inside the active PTX hot-band microkernel likely still leaves a small scoreboard gap after the retime.
- dir_03: Deferred steady-state overlap recovery | bottleneck: Residual handoff overlap and refill timing in the steady-state peeled hot-band path.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
