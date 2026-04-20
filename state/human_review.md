# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 1/10` with `10` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_202755`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/10 human-idea audit against the fresh correct baseline: Tiling is accepted historically, but not as a fresh pivot this round because the repo already proved 64x384 is the best correct macro width for this GPU/shape; Coalescing Access is accepted as baseline because cp.async staging is already 16-byte aligned and the run is not DRAM-bound; Data Reuse is accepted as baseline because the fixed peeled kernel already depends on shared reuse; Async Copy is accepted as baseline because the current pipeline is already cp.async-based; Bank Conflict is deferred to rank-3 because the more immediate limiter on the correct branch is register-driven occupancy rather than feed stalls; L2 Cache swizzle is deferred because lts and dram throughput are both modest; Register Reuse is accepted as the primary family because the stable base is still sitting at only 16.59 active warps with launch__occupancy_limit_registers = 1; Pg2s is accepted as baseline because double-buffer G2S is already present; Ps2r is accepted in spirit via serial micro-panels that reduce simultaneously live B/acc tiles; Stage is accepted as baseline because barrier and mio are already low enough that stage churn is not the first lever. Recommended direction is dir_01 because it keeps the proven 64x384 outer shape while directly attacking the remaining register wall on the correct branch.`
- dir_01: Human idea 7 Register reuse: keep the outer 64x384 hot path, but serialise the inner live set into 2x192 micro-panels | bottleneck: Register pressure and resulting latency-hiding loss on the stable 64x384 PTX hot path.
- dir_02: Human idea 7 Register reuse: if 2x192 still keeps too much live state, split the 64x384 hot path into 3x128 micro-panels | bottleneck: Register pressure first, then possible serialisation overhead if the panel size gets too small.
- dir_03: Human idea 5 Bank conflict: stay on the correct 64x384 path and do a warp-local B-consumer load-order retune with no extra shared or CTA barriers | bottleneck: Operand-delivery efficiency and shared-bank behavior inside the warp-local B consumer path, not DRAM throughput.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
