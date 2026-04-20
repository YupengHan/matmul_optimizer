# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 58/100` with `43` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_084642`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Anchored to measured run 20260420_084554_bf16_gemm_v1_761d868 at 25.473536 ms. Round 56 accepted base at 24.713584 ms remains the target comparison; grouped_rows=16, warmup-order reopen, K32 cadence, extra-live B lookahead, unroll-1 base, CTA-level B repack, and broad shared-memory rewrites are rejected this round.`
- dir_01: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Consumer-side PTX hot-band ordering and export latency in bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel, especially around the grouped-row dispatch and the consumer/export handoff.
- dir_02: Recover overlap behind the accepted wait_group_0 handoff | bottleneck: Async refill overlap in the peeled PTX hot-band path, including the one-sync handoff in the PTX microkernel loop and the peeled hot-stage advance helper.
- dir_03: Smaller locality retune as a closure path | bottleneck: Residual launch-order locality and row-pair adjacency effects in the grouped hot-band consumer path.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
