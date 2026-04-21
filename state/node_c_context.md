# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Reopen The Auxiliary 256x128 Hot-Band Schedule On The Restored Best Base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_183131`
- round loop: `round 6/50`
- hypothesis: `The latest measured specialization run 20260420_183102_bf16_gemm_v1_29a10ec closes the current PTX inner-loop family on the restored grouped-rows-4 lineage: hot-band registers climbed from 200 on the accepted 2e4dd24 base to 242, long-scoreboard stalls jumped from 7.43% to 15.07%, barrier stalls rose from 5.61% to 6.75%, and end-to-end runtime regressed to 25.6650238 ms. The best next move is therefore to accept a materially different hot-band family rather than another PTX-loop tweak. The auxiliary 256x128 branch is the strongest alternate family in measured history, with a 24.69619179 ms result on 20260420_112149_bf16_gemm_v1_9a4bb85, so retuning that schedule on top of the restored 2e4dd24 base offers the best remaining upside.`
- expected bottleneck: `The main risk is that the wider 256x128 CTA can trade away the grouped-row locality win unless its K-loop cadence and export timing are retuned for the current base. If it fails, the signature will be barrier or scoreboard pressure moving from the current PTX hot band into the auxiliary schedule rather than a clean runtime gain.`
- code locations: `src/kernels/bf16_gemm_v1.cu:145-156, src/kernels/bf16_gemm_v1.cu:1576-1664, src/kernels/bf16_gemm_v1.cu:2078-2125`
- risk: `Medium. This is a real family pivot, but it has positive measured ancestry and avoids spending another round on the now-regressed fixed-452-tile PTX specialization path. The main failure mode is repeating the slower naive auxiliary-default restore that later measured 31.86790371 ms, so this should be treated as a schedule retune, not a blind path swap.`
- metrics to re-check: `median_runtime_ms, hot-band kernel gpu__time_duration.sum, hot-band registers per thread, smsp__pcsamp_warps_issue_stalled_long_scoreboard, smsp__pcsamp_warps_issue_stalled_barrier, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it
- `scripts/graph.py` or `scripts/sweep_fixed_main_tiles.py` only when the direction requires minimal workflow glue

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- `src/kernels/bf16_gemm_v1.cu`
