# Round loop

- active: `yes`
- status: `running`
- total rounds: `50`
- completed rounds: `19`
- remaining rounds: `31`
- current round label: `round 20/50`
- auto use recommended: `yes`
- accepted base run id: `20260419_235558_bf16_gemm_v1_be44358`
- accepted base measured commit: `be44358062dd87db8692cf1a8ce8017bab55a65d`
- accepted base runtime: `29.204992 ms`
- started at: `2026-04-19T22:34:28-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Completed round 19/50. Continue with node_b for round 20/50. Accepted base: 20260419_235558_bf16_gemm_v1_be44358 at 29.204992 ms.`

## Last completed round

- round: `19/50`
- direction: `dir_01`
- direction name: `Restore the 128x128 K16 winner and add a register-pressure / launch-bounds hint to chase higher occupancy`
- verdict: `regressed`
- runtime delta: `+28.935681 ms`
- TFLOP/s delta: `-10.958165 TFLOP/s`
- run dir: `runs/20260420_000504_bf16_gemm_v1_f35aea8`
- ncu rep path: `runs/20260420_000504_bf16_gemm_v1_f35aea8/ncu_profile.ncu-rep`
