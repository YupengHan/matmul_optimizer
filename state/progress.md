# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `29a10ec11c08f9648a277030c3340013f3eb8492`
- plateau counter: `3`
- round loop: `round 6/50`
- rounds remaining: `45`
- notes: `Node C build succeeded for round 6/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_183102_bf16_gemm_v1_29a10ec`
- run dir: `runs/20260420_183102_bf16_gemm_v1_29a10ec`
- correctness: `PASS`
- median runtime: `25.665024 ms`
- TFLOP/s: `28.327245 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_183131`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 6/50 diagnosis for 20260420_183102_bf16_gemm_v1_29a10ec. Human-review audit: state/human_review.md currently contains workflow and approval guidance but no concrete user-supplied idea-family bullets to evaluate one by one, so there are no explicit human ideas to accept, defer, or reject this round; ranking is therefore driven by measured evidence. The latest run explicitly rejects more fixed-452-tile PTX hot-loop surgery on this lineage: versus the accepted 20260420_180146_bf16_gemm_v1_2e4dd24 base, the hot-band kernel moved from 200 to 242 registers per thread, long-scoreboard stalls rose from 7.43% to 15.07%, barrier stalls rose from 5.61% to 6.75%, tensor active slipped from 48.16% to 47.90%, and end-to-end runtime regressed from 24.44441605 ms to 25.6650238 ms. Accepted for this round: pivot to alternate hot-band execution families, with the auxiliary 256x128 schedule as the primary branch because it has the strongest positive measured ancestry outside the current PTX microkernel family. Deferred: seam-only launch-split retunes that preserve the existing PTX loop but probably cap out below the accepted best. Rejected for this round: additional PTX-loop handoff, export-live-range, or fixed-shape specialization variants on the restored grouped-rows-4 base.`
- dir_01: Reopen The Auxiliary 256x128 Hot-Band Schedule On The Restored Best Base | bottleneck: The main risk is that the wider 256x128 CTA can trade away the grouped-row locality win unless its K-loop cadence and export timing are retuned for the current base. If it fails, the signature will be barrier or scoreboard pressure moving from the current PTX hot band into the auxiliary schedule rather than a clean runtime gain.
- dir_02: Use The Non-PTX 128x128 Sibling As A Clean Control Path | bottleneck: Because the sibling kernel currently uses plain block ordering instead of the grouped-row physical-to-logical remap, it may give back the locality benefit that made 2e4dd24 fast even if it lowers registers. The expected bottleneck is therefore a trade between reduced scoreboard pressure and weaker L2 / launch-order reuse.
- dir_03: Retune The Hot-Band/Peeled Seam Without Touching The PTX Loop | bottleneck: This branch is bounded by the peeled kernel becoming the new bottleneck. If the seam moves too far upward, the 384-wide peeled path can easily erase any hot-band relief through extra barrier time and worse combined kernel balance.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.473473 ms`, `0.943148x` slower than CUTLASS
