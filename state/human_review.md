# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 37/100` with `64` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_011150`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 37/100 diagnoses run 20260420_011121_bf16_gemm_v1_e0ebab7 at 26.128304 ms on the active 128x128 K16 PTX hot-band branch. The round-36 consumer-side B rewrite is a real mixed signal: runtime regressed only slightly from 26.093568 ms to 26.128304 ms, tensor-active slipped only from 48.43% to 48.03%, and long-scoreboard stayed flat at 1.20%, but barrier rose from 8.05% to 10.95%, short-scoreboard jumped from 1.67% to 5.89%, and DRAM/L2 climbed from 30.93% / 25.77% to 36.86% / 30.64%, even as mio_throttle collapsed from 4.45% to 0.48%. That means the consumer-side B reuse idea has clear signal, but the current sequencing turned one feed bottleneck into a warp-local dependency and synchronization problem instead of improving end-to-end runtime. Human-idea audit for this round, family by family: Tiling is rejected as the primary family because the real 256x128 hot-band promotion already regressed badly and the current 128x128 PTX branch remains the best measured path. Coalescing Access is deferred because the active path already uses 16-byte cp.async wide global movement, and the latest regression is not explained by under-packed global transactions. Data Reuse is accepted, but only in warp-local consumer form; shared-memory A/B reuse is already the baseline and CTA repack remains rejected. Async Copy and Pg2s are accepted only as the existing two-stage baseline; deeper Stage rewrites are rejected again because the earlier K32 / deeper-stage branch lost badly. Bank Conflict is accepted, but only through consumer-side delivery or lighter export, because the current short-scoreboard spike says the issue is where and when fragments are consumed, not a need for more CTA-level shared traffic. L2 Cache is deferred: the latest variant raised DRAM/L2, but launch-order tuning is not the highest-leverage fix until the active PTX branch is stable again. Register Reuse and Ps2r are the primary accepted families because the current cross-row-pair reuse clearly reduced mio_throttle, yet the way it extends fragment lifetime is probably too aggressive. Stage is deferred beyond the current two-stage baseline; only bounded wait/barrier sequencing cleanup is supported this round. Because the target remains 20 ms rather than merely beating the 25.917889 ms CUTLASS baseline, the ranking stays centered on the active PTX hot-band branch and favors preserving the observed B-reuse signal while removing the new short-scoreboard and barrier cost.`
- dir_01: Keep the active PTX B-fragment reuse, but rewrite warp-local sequencing to shrink the new short-scoreboard and barrier cost | bottleneck: Warp-local consumer sequencing and fragment live-set pressure in the active PTX hot-band branch, where the current B-reuse schedule traded mio_throttle for short-scoreboard, extra synchronization exposure, and higher DRAM/L2 traffic.
- dir_02: Trim the active PTX hot-band export path and c_shared round-trip now that feed-side mio pressure is much lower | bottleneck: Epilogue-side shared-memory and LSU overhead on the active PTX hot band, especially c_shared bank writes and synchronization after the MMA loop.
- dir_03: Back off to a narrower consumer-side B-reuse variant instead of the fully fused two-row-pair reuse | bottleneck: Over-aggressive warp-local B reuse on the active PTX branch, where the current fused two-row-pair schedule may be over-optimizing MIO at the expense of dependency depth and exposed synchronization.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
