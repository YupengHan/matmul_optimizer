# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 14/100` with `87` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_000409`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 14/100 audit: round 13 cleanly falsified the A-then-B PTX handoff retime on the correct PTX surface. The dominant kernel stayed `bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>`, but runtime regressed by 0.320559 ms and barrier rose from 5.43% to 6.29%. The current source differs from the round-12 best PTX surface by essentially one refill-order hunk, so the next action should be to restore that best surface first, then continue active-PTX exploration from a valid anchor while keeping the grouped_rows=8 round-history fallback alive.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Known-negative handoff ordering on the active PTX hot-band loop, where the A-then-B future refill increases effective barrier cost enough to overwhelm any scoreboard reduction.
- dir_02: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual PTX hot-band control-path overhead and consume-order friction on the restored one-K 128x128 PTX surface, beyond the already-closed A-then-B handoff variant.
- dir_03: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Consumer-side ordering and grouped-row locality inside the PTX hot-band microkernel under the grouped_rows=8 regime.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
