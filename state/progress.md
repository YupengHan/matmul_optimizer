# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `778a0b475a3fbcfd5a0f3fecc8381784fa832256`
- plateau counter: `3`
- round loop: `round 19/20`
- rounds remaining: `2`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 19/20.`

## Latest measured custom run

- run id: `20260419_195339_bf16_gemm_v1_778a0b4`
- run dir: `runs/20260419_195339_bf16_gemm_v1_778a0b4`
- correctness: `FAIL`
- median runtime: `30.236128 ms`
- TFLOP/s: `24.044726 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_195407`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 19 human-idea audit against measured evidence: Tiling is accepted and already embodied by the active 256x128 CTA / 64x64 warp branch; Coalescing Access is accepted as baseline because the kernel is already on 16-byte cp.async loads and the latest run is not transaction-bound; Data Reuse is accepted as baseline because the branch already depends on shared-memory reuse for both operands; Async Copy is accepted as baseline because cp.async is already central to the pipeline; Bank Conflict is deferred this round except as the fallback family because the current blocker is correctness rather than shared-feed throughput; L2 Cache swizzle is deferred because lts throughput is only 36.08% and DRAM is 21.33%, so cache is not the dominant limiter; Register Reuse is accepted as the primary family because the half-panel branch is still the only path that broke below 100 regs and lifted active warps into the low-30s; Pg2s is accepted as baseline because double-buffer global-to-shared prefetch is already present; Ps2r is accepted as the next family after correctness because replaying A across two serial half panels is now the clearest avoidable tax; Stage is accepted as baseline because the two-stage pipeline is already doing its job and the current evidence does not justify stage-count churn. Recommended direction is dir_01 because with only two rounds left, the penultimate round should either make the high-ceiling half-panel family correct or decisively prove it is not salvageable.`
- dir_01: Human idea 7 Register reuse: keep the half-panel family and close the remaining correctness gap by single-sourcing warp ownership end to end | bottleneck: Residual half-panel address-contract mismatch in the shared-to-fragment or fragment-to-export path, not DRAM bandwidth. The runtime and occupancy signal say the family is viable; correctness is the blocking bottleneck.
- dir_02: Human idea 9 Ps2r: fuse the two 32-column passes inside one K-loop so each staged A tile is consumed twice before advancing | bottleneck: Barrier and shared/A-feed replay overhead caused by running the left and right half panels as two full passes. Successful fusion should cut barrier pressure and short-scoreboard pressure without giving back the occupancy gain.
- dir_03: Human idea 5 Bank conflict fallback: return to the accepted 64x384 path and try a warp-local B-consumer transform with no extra CTA repack | bottleneck: Shared/L1/bank behavior on the stable 64x384 hot path rather than occupancy. This is a lower-ceiling but lower-correctness-risk fallback.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
