# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 8/10` with `3` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_213118`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 8 human-idea audit after the negative L2 experiment and the restore to the accepted implementation surface: Tiling stays accepted because the sweep already established the 64x384 hot band as the best macro width on this GPU; Coalescing Access, Data Reuse, Async Copy, and Pg2s remain accepted as baseline infrastructure because the current source already uses 16-byte cp.async plus shared reuse for both operands; L2 Cache is now explicitly rejected for this loop because round 7's grouped CTA remap regressed runtime to 31.310287 ms, made the hot-band kernel slower at about 41.66 us, left L2 throughput essentially flat near 19.07, and increased DRAM pressure instead of reducing it; Stage is also rejected for the next move because round 6 already proved the fixed-shape control refactor can restore correctness yet still regress; Bank Conflict / warp-local consumer transform is promoted to the primary family because the control-path and cache-path experiments were both negative while the current restored source is back on the accepted correct branch; Producer/consumer warp specialization remains a secondary orchestration family; Ps2r stays tertiary because the branch is already near 167 regs/thread. Recommended direction dir_01 therefore goes back to the restored accepted base and changes only the warp-local B consumer path, with strict guardrails: no extra shared tile, no extra CTA barrier, and no stage-depth loss.`
- dir_01: Human idea bank-conflict follow-through: warp-local B consumer transform on the restored accepted base | bottleneck: Warp-local shared/L1 operand delivery and bank behavior on B fragment loads in the true hot-band kernel.
- dir_02: Warp-specialized producer/consumer on the restored 256x128 hot kernel | bottleneck: All-warps staging and handoff overhead on the hot-band kernel under one-block register-limited occupancy.
- dir_03: Human idea Ps2r: one-fragment shared-to-register lookahead in the full-width 64x64 hot sweep | bottleneck: Warp-local shared-to-register delivery latency inside the hot-band 64x64 sweep.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
