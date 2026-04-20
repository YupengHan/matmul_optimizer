# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `3dd4394d5113e6c6f6f2cc1e37c32dad490af6c4`
- plateau counter: `11`
- round loop: `round 10/20`
- rounds remaining: `11`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 10/20.`

## Latest measured custom run

- run id: `20260419_181807_bf16_gemm_v1_3dd4394`
- run dir: `runs/20260419_181807_bf16_gemm_v1_3dd4394`
- correctness: `PASS`
- median runtime: `488.546341 ms`
- TFLOP/s: `1.488128 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_182158`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 10 is a revert-and-continue move, not a clean continue and not yet a pivot. The Stage family should be continued from the round-8 checkpoint and explicitly not from the current round-9 code shape. Round 8 is still the relevant family evidence: it was correct, it slashed barrier, long-scoreboard, and mio, and it reduced registers and shared-memory budget without destroying tensor issue. Round 9 then tried to force the branch under the occupancy cliff by splitting the hot pipeline and export path into __noinline__ helpers. The result was catastrophic but informative: occupancy_limit_registers opened to 2 and active warps rose to 33.22, yet tensor active collapsed to 3.36, long scoreboard exploded to 40.26, mio to 18.47, and DRAM throughput to 90.96. That means the occupancy change was purchased by a broken code shape, not a healthier hot kernel. The correct diagnosis is therefore to reject the round-9 reg-squeeze implementation strategy, restore the round-8 inline Stage checkpoint, and only then decide whether Stage still merits further refinement.

Human idea audit for this round:
1. Tiling (256x128 block, 64x64 warp): reject-for-this-round. The existing tile sweep still says 64x384 is the measured sweet spot, and the current failure is code-shape-driven rather than tile-shape-driven.
2. Coalescing Access: defer. Wide 16-byte global access is already present, so it is not the first lever to pull from this failure.
3. Data Reuse: accept-now as an already adopted baseline, not as a new primary family. Shared-memory reuse of A and B is not what failed in round 9.
4. Async Copy: accept-now within the Stage family, but only through the round-8-style inline pipeline. The round-9 helper split is negative evidence against further codegen surgery here.
5. Bank Conflict: reject-for-this-round. The current catastrophic signature is not a bank-conflict signature, and prior B-feed experiments were negative.
6. L2 Cache: reject-for-this-round. The measured failure is dominated by a broken hot-kernel code shape, not by an L2 hit-rate problem.
7. Register Reuse: accept-now as the top pivot candidate if Stage recovery fails. It attacks residual warp-issue efficiency without reopening the failed feed-path rewrites.
8. Pg2s: accept-now only as existing baseline behavior. Global-to-shared double buffering is already present and is not the new decision point.
9. Ps2r: defer as the safer fallback family. It showed earlier positive-but-insufficient evidence and is still more credible than a fresh structural pivot if Stage must be demoted.
10. Stage: accept-now, but only as a revert-and-continue family. Continue the family from the round-8 checkpoint; abandon building on the current round-9 __noinline__ codegen.`
- dir_01: Human idea 10 Stage: revert the catastrophic __noinline__ reg-squeeze split and continue from the round-8 checkpoint | bottleneck: Broken code generation and likely spill-like memory domination from the __noinline__ split, visible as extreme DRAM throughput, long scoreboard, and mio rather than useful tensor issue.
- dir_02: Human idea 7 Register reuse: pivot to warp-local RLRL accumulator traversal on the stable 64x384 PTX base | bottleneck: Warp-internal issue order and fragment reuse inefficiency inside the 64x384 PTX accumulate sweep, showing up mainly as residual tensor underfill and short-latency scheduling waste rather than CTA-level feed stalls.
- dir_03: Human idea 9 Ps2r: return to the earlier inline shared-to-register lookahead as the safer latency-hiding fallback | bottleneck: Shared-to-register latency hiding inside the PTX hot sweep, with long scoreboard as the main metric and tensor active as the payoff metric.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `6.083199 ms`, `1.234710x` slower than CUTLASS
