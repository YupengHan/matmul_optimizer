# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 5/5` with `1` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_100543`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5/5 diagnosis prepared from near-hit run 20260419_100457_bf16_gemm_v1_6dd39ad. Evidence hierarchy: accepted base 16a98f7 remains nominally best at 37.285807 ms; round 1 two-level B staging regressed badly; round 2 phased 64x384 micro-panels regressed badly; round 3 warp-specialized staging improved one symptom but stayed much slower; round 4 fixed-shape peeled hot kernel nearly matched the base at 37.373951 ms while raising tensor active and lowering barrier stall. Final-round ranking therefore treats the peeled hot path as the most credible basis and prioritizes complementary one-round changes over reopening the clearly failed rewrite families.`
- dir_01: Re-land the peeled hot kernel and trim the c_shared export path | bottleneck: Epilogue-side shared/export traffic after the peeled steady-state loop improves control overhead.
- dir_02: Re-land the peeled hot kernel and deepen single-skew cp.async overlap | bottleneck: Copy-latency / short-scoreboard exposure in the peeled steady-state loop.
- dir_03: Re-land the peeled hot kernel with a bounded single-skew B stride retune | bottleneck: Residual B-side staging inefficiency in the current single-skew layout, not a full feed-path redesign.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
