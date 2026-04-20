# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 41/100` with `60` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_014548`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 41/100 should stay centered on the accepted round-38 PTX hot-band branch, not on the noisy 27.088384 ms measurement alone. The main-agent comparison between commit e26d834 and commit 09d3544 found no behavioral source change at the active PTX microkernel call site, only formatting, and the headline NCU metrics are effectively unchanged. That makes round 40 a run-to-run variance event, not evidence that the round-38 branch was wrong. Human-idea audit for this round: Tiling is rejected as the primary move because the real active 256x128 CTA / 64x64 warp promotion already regressed badly on the default path; Coalescing Access is accepted as already implemented through wide 16-byte async copy and does not explain the remaining gap; Data Reuse is accepted and stays fundamental because the active branch's win still depends on explicit warp-local B reuse; Async Copy is accepted only as the current working baseline, while deeper staging is deferred because earlier heavier pipeline changes regressed; Bank Conflict is accepted and remains important through both the padded export scratch and any future consumer-side lane mapping cleanup; L2 Cache is deferred because grouped ordering helped an older branch but does not explain the accepted PTX branch's current residual stalls; Register Reuse is accepted and remains a core lever on the consumer side; Pg2s is accepted as already present in the two-stage cp.async pipeline; Ps2r is accepted and still relevant for warp-local B delivery; Stage is accepted only in the narrower sense of steady-state sequencing cleanup, while deeper or more complex staging is rejected for this round. The ranking is still aimed at the real target of sub-20 ms, not merely at edging out the 25.917889 ms CUTLASS baseline.`
- dir_01: Keep The Accepted PTX Branch And Make The Steady-State Sequence More Explicit | bottleneck: Synchronization and orchestration overhead in the active PTX steady-state loop. The accepted branch has already collapsed mio_throttle, so the next runtime limiter is the combination of CTA barrier cost and warp-local short scoreboard that comes from the current wait / sync / recursive consume sequence.
- dir_02: Keep The Accepted PTX Branch And Refine The Export Scratch Path | bottleneck: c_shared round-trip and shared-memory export overhead after the hot loop, especially bank writes, LSU wavefront pressure, and paired stage bookkeeping in the PTX-only export helpers.
- dir_03: Keep The Accepted B-Reuse Pattern But Narrow The Consumer-Side Delivery Tweak | bottleneck: Warp-local B-fragment delivery and register residency inside the active PTX microkernel. The current branch already solved the old mio problem, so the question is whether a narrower consumer-side variant can keep that win while reducing scoreboard pressure.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
