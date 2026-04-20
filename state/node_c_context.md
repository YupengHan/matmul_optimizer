# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Tighten Grouped-Row L2 Feed In The 128x128 PTX Hot Band`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_073749`
- round loop: `round 47/100`
- hypothesis: `Round 46's grouped-row traversal already proved that hot-band block order was the right locality lever: median runtime dropped from 26.892288 ms to 25.677312 ms, became the new best custom run, and moved past the local CUTLASS baseline while tensor active stayed flat at 48.24 -> 48.22. The next win is likely not more raw math scheduling, but a narrower follow-on that keeps the grouped-row mapping and further improves how adjacent CTAs reuse B/A lines and feed shared memory, because dram throughput collapsed to 12.90% and lts throughput recovered to 29.45% while mio_throttle still sits at 4.67%.`
- expected bottleneck: `Residual hot-band L2-to-shared feed inefficiency in the dominant 128x128 PTX microkernel, showing up as remaining mio_throttle plus modest shared-bank pressure even after locality improved.`
- code locations: `src/kernels/bf16_gemm_v1.cu: kFixedHotBandGroupedRows and the grouped physical_pid -> logical_block_{x,y} remap in bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel, src/kernels/bf16_gemm_v1.cu: stage_b_shared_tile_async and b_shared_col_from_logical for hot-band B staging layout, src/kernels/bf16_gemm_v1.cu: the hot-band launch path around launch_fixed_hot_band_by_tile_n and the fixed 128x128 PTX microkernel dispatch`
- risk: `Changing CTA traversal or feed order can easily give back the grouped-row locality gain, especially if a more aggressive group size or remap improves L2 reuse for one operand but worsens shared feed cadence or tail behavior. This is the best-ranked path only if the implementation stays narrow and preserves the accepted 128x128 PTX microkernel shape.`
- metrics to re-check: `median runtime and TFLOP/s with the user target still set to <20 ms, dram__throughput.avg.pct_of_peak_sustained_elapsed, lts__throughput.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed and l1tex__data_bank_writes.avg.pct_of_peak_sustained_elapsed on the hot-band kernel`

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

- no tracked dirty paths at prepare time
