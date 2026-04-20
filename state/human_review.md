# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 55/100` with `46` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_083324`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Latest measured run: 20260420_083244_bf16_gemm_v1_66273be at 24.896433 ms. Accepted human-idea families for this round: Register Reuse: Right Left Right Left, Ps2r, Bank Conflict, and L2 Cache: swizzle access mode to increase L2 cache hit ratio. Deferred but still live: Async Copy, Pg2s, Stage. Rejected for this round: reopening the warmup-order branch, K32 cadence, extra-live B lookahead, unroll-1 base, and any CTA-level B repack or extra shared tile. dir_01 is the recommended direction because it targets the PTX hot-band consume boundary rather than macro tiling or CTA staging.`
- dir_01: PTX hot-band consume retime | bottleneck: PTX hot-band consumer ordering is leaving register reuse and shared-memory bank behavior suboptimal after the producer side has already been tuned.
- dir_02: Steady-state cp.async wait/commit retime | bottleneck: Producer/consumer handoff in the steady-state cp.async loop still has timing slack, but the warmup branch is no longer the main target.
- dir_03: Hot-band launch-order refinement | bottleneck: Launch-order locality across the hot band still leaves L2 reuse on the table even after the grouped-row baseline.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
