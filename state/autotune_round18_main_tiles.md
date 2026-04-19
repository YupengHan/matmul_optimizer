# Fixed Main Tile Sweep

- timestamp: `2026-04-19T08:28:48.993401+00:00`
- runner: `/home/aice/Desktop/matmul_optimizer/build/custom_runner`
- dataset dir: `/home/aice/Desktop/matmul_optimizer/artifacts/datasets/fixed_bf16_gemm_v1`
- benchmark case: `case_00_seed_3407`
- correctness cases: `case_00_seed_3407, case_01_seed_9713, case_02_seed_1729`
- env var: `MATMUL_FIXED_MAIN_TILE_N`
- default fixed path when unset: `64x384 main over 7680 columns + 64x96 tail`
- override fixed path when set: `64x<TILE_N> main over 7680 columns + 64x96 tail`
- accepted base run id before promotion: `20260419_011243_bf16_gemm_v1_33e1461`
- accepted base runtime before promotion: `41.53497696 ms`
- warmup / iters: `10` / `30`
- flush cache MiB: `256`

## Best Candidate

- tile_n: `384`
- median runtime (ms): `38.67801666`
- TFLOP/s: `18.79670894`
- delta vs accepted round-17 base: `-2.85696030 ms`
- recommendation: `promote 64x384 main over 7680 columns plus the 64x96 tail to the default fixed-shape path for round 18 node_a validation`

## Insights

- The hot-band sweep is not monotonic. Runtime improves sharply from `32 -> 256`, regresses at `320`, reaches its minimum at `384`, then falls apart again at `480`.
- `64x192` over the full 7680-column hot band measures `41.98348618 ms`, so the old default `64x192 + 64x128 + 64x96` is better than a flat `192` override, but it is still materially slower than `256` and `384`.
- `64x384` appears to be the sweet spot for this GPU and shape: it cuts hot-band CTA count aggressively without paying the heavier pressure penalty that shows up at `480`.
- The current follow-up for node_a is straightforward: validate the promoted default `64x384 + 64x96` path with the full graph workflow and Nsight Compute capture.

## Results

| tile_n | correctness | perf | median ms | p10 ms | p90 ms | TFLOP/s | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 32 | PASS | PASS | 73.20727921 | 72.28999863 | 76.61998367 | 9.93097175 | ok |
| 64 | PASS | PASS | 53.61763191 | 52.56417427 | 56.28293037 | 13.55933479 | ok |
| 96 | PASS | PASS | 47.57759857 | 46.88916473 | 49.85240288 | 15.28070864 | ok |
| 128 | PASS | PASS | 44.68172836 | 43.88229141 | 46.55594711 | 16.27106758 | ok |
| 160 | PASS | PASS | 43.25427246 | 42.71493378 | 44.11699142 | 16.80803723 | ok |
| 192 | PASS | PASS | 41.98348618 | 41.37523346 | 42.98342133 | 17.31679496 | ok |
| 256 | PASS | PASS | 40.65945625 | 40.19230423 | 41.13223801 | 17.8806971 | ok |
| 320 | PASS | PASS | 42.41771317 | 41.72943306 | 43.42476692 | 17.13952421 | ok |
| 384 | PASS | PASS | 38.67801666 | 38.13918724 | 39.56817932 | 18.79670894 | ok |
| 480 | PASS | PASS | 43.57734489 | 43.06002045 | 44.22137451 | 16.6834263 | ok |
