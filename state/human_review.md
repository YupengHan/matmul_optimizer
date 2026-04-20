# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 18/20` with `3` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_194057`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 18 is still a continue-family move on the half-panel branch. The reason is not optimism; it is the measured evidence. Even while still incorrect, the current hot bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel kept the register/occupancy breakthrough from round 17 and improved it slightly: launch__registers_per_thread is 92, launch__occupancy_limit_registers is 2, sm__warps_active is 32.70, sm__pipe_tensor_cycles_active is 43.55, and the hot-kernel time improved again. Runtime also recovered from 32.9149 ms to 30.8762 ms, much closer to the accepted 30.0528 ms, despite correctness still failing. That is exactly the signature of a branch that is incomplete rather than invalid. The remaining problem is that correctness is still broken and feed tax is still high: gpu__compute_memory_throughput stays around 61.40, barrier is back above 21, and short-scoreboard remains elevated. With only three rounds left, that means the priority should be correctness root-cause repair first, not another new optimization family. A-side compact staging is plausible, but only after the branch is correct.

Human idea audit for round 18:
1. Tiling: accept-now as the outer family. The 256x128/64x64 mainline is still the only proven structural path.
2. Coalescing Access: defer. The current limiting issue is not generic load width; it is pass-local half-panel correctness and replayed movement.
3. Data Reuse: accept-now as a supporting follow-up. Reusing A across the two half-panel passes is the next coherent feed-tax lever after correctness.
4. Async Copy: accept-now as supporting infrastructure. The recommended direction keeps async copy but makes its panel layout auditable.
5. Bank Conflict: defer as the conservative fallback only. Shared-load retuning is real, but it is lower ceiling than fixing the live half-panel branch.
6. L2 Cache: reject-for-this-round. The current branch is not being blocked by an isolated cache-hint issue.
7. Register Reuse: accept-now and rank first. This family still owns the only real register-wall breakthrough in the loop.
8. Pg2s: accept-now and rank second. A-side producer replay is now the next obvious feed tax once correctness is fixed.
9. Ps2r: reject-for-this-round. The data says this branch is no longer waiting on shared-to-register lookahead.
10. Stage: reject-for-this-round. There is no remaining budget to reopen a weaker family.

Primary decision: continue Human idea 7, but use this round to fix correctness root cause while preserving the current 92-register / 2-block-per-SM shape. If that succeeds, round 19 can spend its budget on A-side producer reuse instead of first having to re-earn correctness.`
- dir_01: Human idea 7 Register reuse: continue the half-panel family, but spend this round on correctness root-cause repair while preserving the 92-reg / 2-block signal | bottleneck: Correctness bug in the half-panel pass-local mapping and orchestration, not lack of more occupancy or more feed bandwidth.
- dir_02: Human idea 8 Pg2s: after correctness, stop replaying the A producer path twice by reusing A stages across the two half-panel passes | bottleneck: Replay of the A-side producer path across the two half-panel passes, inflating compute-memory throughput even after B-side compaction.
- dir_03: Human idea 5 Bank conflict: abandon the half-panel branch and return to the accepted base for a bounded local shared-load retune | bottleneck: Residual short-scoreboard and shared-load pressure on the accepted-base 256x128/64x64 path after abandoning the broken high-ceiling branch.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
