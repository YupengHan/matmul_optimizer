# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 50/100` with `51` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_075727`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `- Accepted best base remains round 47's grouped-row=8 PTX hot band at 25.529328 ms (`20260420_074331_bf16_gemm_v1_17a33b2`), and every new direction is ranked relative to that base rather than the regressed round-49 state.
- B-fragment lookahead stops here: round 48 regressed to 25.759745 ms, so do not keep digging the extra-live-B / rolling-window Ps2r branch.
- K32 cadence stops here: round 49 regressed hard to 31.728224 ms and also degraded tensor active to 39.98 while raising long_scoreboard to 6.11 and mio_throttle to 5.81, so do not continue stage-cadence mining on that branch.
- Next-round narrow recommendation: `dir_01` is the most constrained new move, namely restore the accepted grouped-row=8 K16 PTX hot band and trim export or operand live range without adding a new stage form or extra B-fragment retention.
- Coalescing Access: not the lead family now; the grouped-row=8 accepted base already captured the major access-order win, so another broad coalescing pass is lower value than accepted-base restoration.
- Data Reuse: still valid, but only through narrow grouped-row=8-preserving traversal refinements; it is not permission to reopen the failed B-lookahead family.
- Async Copy: already present and functional via `cp.async`; the evidence says the next round should not add a fresh async-copy mechanism.
- Bank Conflict: worth keeping as a third-ranked micro-tweak because shared-bank traffic is still visible, but it remains secondary to restoring the accepted base and trimming live range.
- L2 Cache: still real because round 47 was a true win, so the family stays alive only as a small grouped-row=8 locality refinement instead of another broad remap.
- Register Reuse: promoted to the top remaining new family, but only in the narrow form of export or operand lifetime trimming on the accepted K16 PTX path.
- Pg2s: not the current limiter; DRAM stayed low enough that a new global-to-shared rewrite is not the next best use of a round.
- Ps2r: explicit stop for the B-fragment lookahead variant after round 48; if any reuse work remains, it must avoid keeping extra B fragments live.
- Stage: explicit stop for the K32 cadence family after round 49; stage experimentation is no longer the next branch to mine.
- Target framing stays unchanged: the user target is still <20 ms, not just beating CUTLASS.`
- dir_01: Hold Grouped-Row=8 K16 Fixed And Trim PTX Export Or Operand Live Range | bottleneck: Register-pressure and latency-hiding loss inside the dominant grouped-row=8 128x128 PTX hot-band microkernel, especially around export scratch and operand lifetime rather than new pipeline depth.
- dir_02: Keep Grouped-Row=8 And Probe One Narrow CTA-Order Or L2 Reuse Refinement | bottleneck: Residual L2 locality and cross-CTA reuse efficiency inside the accepted grouped-row=8 PTX hot band after the main access-order win has already been harvested.
- dir_03: Preserve The Accepted Base And Test Only A Shared-Layout Or Bank-Conflict Micro-Tweak | bottleneck: Shared-memory layout friction in the dominant grouped-row=8 PTX hot band, expressed as avoidable bank traffic and MIO-side pressure rather than insufficient global-memory bandwidth.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
