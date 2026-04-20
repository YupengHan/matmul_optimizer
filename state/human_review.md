# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 8/20` with `13` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_180512`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Audit of the 10 human idea families for round 8 on the current round-7 stage-branch source and measured run 24b96ad. Recommendation type: continue-family move. The diagnosis explicitly keeps human idea 10, Stage, alive for another round because the stall signature changed too dramatically to treat it as a dead family after one broken implementation. Per-idea status: (1) Tiling 256x128 block / 64x64 warp = defer, because it is a structural family with possible ceiling, but the live stage branch provides much stronger direct signal right now than abandoning the 64x384 PTX line before repairing correctness. (2) Coalescing Access = accept-now as already present in the current kernel through 16-byte wide accesses; not the current bottleneck. (3) Data Reuse through shared memory = accept-now as already core and directly relevant to the current export-storage ownership problem. (4) Async Copy = accept-now as already core; the stage family is its deepest current expression. (5) Bank Conflict = defer, because the current dominant issue is correctness/handoff on the stage branch, not bank behavior. (6) L2 Cache swizzle = reject-for-this-round, because the current measurements do not support cache locality as the main problem. (7) Register Reuse RLRL = defer, because it is plausible later but lower priority than repairing the live stage branch. (8) Pg2s = accept-now as already present and foundational to the stage family. (9) Ps2r = defer, not reject; it remains the bounded fallback family because it produced correct runs and one real signal, but it is not the primary branch while idea 10 still looks fixable. (10) Stage multi-buffer = accept-now and recommended again, because round 7 combined major reductions in barrier, long-scoreboard, mio, and registers with a suspicious correctness bug around overlaid export storage. Additional negative evidence still in force: no explicit half-panel mma.sync compute rewrite, no pair-compaction retry, no panelized B-load reorder, no helper/lifetime compaction as the main lever, and no near-neighbor handoff-retime retry.`
- dir_01: Human idea 10 Stage: repair the 3-stage family with an explicit terminal CTA handoff before export overlay reuse | bottleneck: The main blocker looks like a correctness and data-handoff bug in the stage/export ownership transition, not a lack of stage-family upside.
- dir_02: Human idea 10 Stage: keep the 3-stage pipeline but remove b_shared export aliasing as the ownership model | bottleneck: The current stage branch may be corrupting correctness and performance through unsafe scratch ownership rather than through the stage depth itself.
- dir_03: Human idea 9 Ps2r: bounded fallback pivot to the last correct feed-path family | bottleneck: Warp-local shared-to-register latency remains a real but lower-ceiling limiter that can still offer controlled gains if the stage branch is not repairable.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
