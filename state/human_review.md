# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 34/100` with `67` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_004413`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 34 is ranked against a clear failure on the real hot path. Round 33 promoted bf16_gemm_v1_tensor_core_fixed_hot_band_128x128x32_kernel onto the default fixed-shape branch and regressed the benchmark from the accepted 26.924031 ms base (run 20260420_002759_bf16_gemm_v1_1b9dbe3, tensor-active 48.56, barrier 8.13, long-scoreboard 1.31, mio 4.44) to 31.684608 ms (run 20260420_004325_bf16_gemm_v1_bbb7383, tensor-active 40.12, barrier 9.55, long-scoreboard 6.02, mio 5.29). That means the previous round's active-path Async Copy + Pg2s + Stage expansion should be rejected for now: the extra two-K-tile staging increased orchestration cost instead of hiding latency. Human-idea audit for this round: Tiling is ACCEPTED, but only on real active-path experiments, so dir_01 restores the accepted K16 base and promotes the existing 256x128 CTA / 64x64 warp branch instead of dead-path grouped_rows or more K32 staging. Coalescing Access is ACCEPTED because the viable directions keep the existing 16-byte cp.async / wide global movement rather than scalarizing loads. Data Reuse is ACCEPTED only through the current shared-memory reuse model; no CTA-level repack is recommended. Async Copy is DEFERRED to the accepted double-buffer form and REJECTED as a deeper active-path rewrite this round. Bank Conflict is ACCEPTED as a secondary family in dir_02 and dir_03 through consumer-side delivery and export/shared cleanup. L2 Cache is DEFERRED: grouped ordering helped earlier, but the latest regression was not an L2-hit-ratio story. Register Reuse is ACCEPTED, especially in the PTX branch and existing RLRL-style 64x64 accumulation helpers. Pg2s is DEFERRED to the proven two-stage K16 path; Ps2r is ACCEPTED only for a dedicated PTX microkernel branch; Stage is REJECTED beyond the proven K16 depth on the active path until a restored base is back in place. The optimization target remains 20 ms, not merely the 25.92 ms CUTLASS baseline, so the ranking favors real-path changes with larger ceiling over minor parameter churn.`
- dir_01: Restore the 26.924 ms K16 base and promote the real 256x128 CTA / 64x64 warp hot-band branch onto the default path | bottleneck: Tensor Core under-utilization caused by the current active hot-band geometry and control path, not by raw DRAM bandwidth. The target is to raise tensor-active and useful work per CTA without reintroducing the K32 feed/orchestration penalties.
- dir_02: Restore the accepted base and open a dedicated active hot-band PTX microkernel branch | bottleneck: Feed/orchestration overhead at the active hot-band consumer boundary, especially shared-to-fragment delivery and export traffic that currently dilutes tensor issue even on the better K16 branch.
- dir_03: Restore the accepted base and attack c_shared export plus shared-bank overhead inside the existing K16 hot-band path | bottleneck: Shared-memory and epilogue/export overhead that keeps tensor issue below its ceiling even when the hot-band steady-state itself is closer to correct than the failed K32 branch.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
