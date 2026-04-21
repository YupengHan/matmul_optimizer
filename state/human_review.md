# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 13/100` with `88` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_235953`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 13/100 audit: round 12 repaired the search-surface mismatch and restored `bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>` as the dominant measured hot-band launch, producing a new best custom runtime at 24.16427231 ms. The current source is now semantically aligned with the previous best-known PTX surface, so restore and export-cleanup families are absorbed again and should be filtered out for this round. The ranking therefore returns to genuinely unabsorbed active-PTX follow-ons, while keeping one round-history PTX alternate alive in the live queue.`
- dir_01: Steady-state Barrier / Handoff Retime | bottleneck: Residual wait-group and barrier cadence in the active PTX hot-band steady-state loop, especially the handoff between MMA issue completion and future-tile refill.
- dir_02: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual PTX hot-band control-path overhead and consume-order friction inside the active one-K 128x128 microkernel, beyond the already-absorbed export cleanup and exact restore.
- dir_03: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Consumer-side ordering and grouped-row locality inside the PTX hot-band microkernel, especially grouped CTA mapping and the export handoff under the grouped_rows=8 regime.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
