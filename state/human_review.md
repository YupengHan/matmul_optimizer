# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `awaiting_direction_selection_for_node_c`
- round loop: `round 4/5` with `2` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_095729`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4/5 diagnosis prepared from run 20260419_095653_bf16_gemm_v1_f237679. Evidence hierarchy: accepted base 16a98f7 at 37.285807 ms remains the reference; round-1 two-level B staging and round-2 phased 64x384 micro-panels both regressed badly; round-3 warp-specialized staging improved over those failed branches and cut mio_throttle sharply, but it still remained meaningfully slower than the accepted base, so it is treated as negative evidence for stacking forward. Ranking therefore pivots to base-oriented steady-state specialization, epilogue trimming, and only a bounded wait/barrier retune.`
- dir_01: Peel a fixed-shape steady-state hot kernel for 6464x7776x7232 | bottleneck: Generic steady-state loop/control overhead diluting tensor issue on the fixed-shape hot path.
- dir_02: Trim the c_shared epilogue/export path on the restored base | bottleneck: LSU/shared writeback pressure in the hot epilogue rather than feed-path or live-set shape.
- dir_03: Apply a bounded cp.async wait/barrier retune to the restored single-skew base | bottleneck: Copy-pipeline wait/barrier scheduling in the accepted base rather than B layout or live-set shape.

## Active direction

- selected direction: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`
