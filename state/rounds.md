# Round loop

- active: `yes`
- status: `round_in_progress`
- total rounds: `10`
- completed rounds: `5`
- remaining rounds: `5`
- current round label: `round 6/10`
- auto use recommended: `yes`
- accepted base run id: `20260419_202711_bf16_gemm_v1_5135c1d`
- accepted base measured commit: `5135c1d6edb580191a96d8c6d9b47cb3ec8b96be`
- accepted base runtime: `30.310320 ms`
- started at: `2026-04-19T20:27:38-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Executing round 6/10.`

## Last completed round

- round: `5/10`
- direction: `dir_01`
- direction name: `Human idea 5/7 Bank conflict + internal-tile order: keep the correct 256x128 hot kernel, but change the 64x64 warp-consumer order to Right/Left/Right/Left`
- verdict: `improved`
- runtime delta: `-0.023553 ms`
- TFLOP/s delta: `+0.018308 TFLOP/s`
- run dir: `runs/20260419_210551_bf16_gemm_v1_61be2e8`
- ncu rep path: `runs/20260419_210551_bf16_gemm_v1_61be2e8/ncu_profile.ncu-rep`
