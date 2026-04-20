# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `66273be4ab02d93dca25251ada08f52ec95cdfd9`
- plateau counter: `2`
- round loop: `round 55/100`
- rounds remaining: `46`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 55/100.`

## Latest measured custom run

- run id: `20260420_083244_bf16_gemm_v1_66273be`
- run dir: `runs/20260420_083244_bf16_gemm_v1_66273be`
- correctness: `PASS`
- median runtime: `24.896433 ms`
- TFLOP/s: `29.201751 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_083324`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Latest measured run: 20260420_083244_bf16_gemm_v1_66273be at 24.896433 ms. Accepted human-idea families for this round: Register Reuse: Right Left Right Left, Ps2r, Bank Conflict, and L2 Cache: swizzle access mode to increase L2 cache hit ratio. Deferred but still live: Async Copy, Pg2s, Stage. Rejected for this round: reopening the warmup-order branch, K32 cadence, extra-live B lookahead, unroll-1 base, and any CTA-level B repack or extra shared tile. dir_01 is the recommended direction because it targets the PTX hot-band consume boundary rather than macro tiling or CTA staging.`
- dir_01: PTX hot-band consume retime | bottleneck: PTX hot-band consumer ordering is leaving register reuse and shared-memory bank behavior suboptimal after the producer side has already been tuned.
- dir_02: Steady-state cp.async wait/commit retime | bottleneck: Producer/consumer handoff in the steady-state cp.async loop still has timing slack, but the warmup branch is no longer the main target.
- dir_03: Hot-band launch-order refinement | bottleneck: Launch-order locality across the hot band still leaves L2 reuse on the table even after the grouped-row baseline.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.022401 ms`, `0.960552x` slower than CUTLASS
