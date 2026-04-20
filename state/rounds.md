# Round loop

- active: `yes`
- status: `round_in_progress`
- total rounds: `10`
- completed rounds: `2`
- remaining rounds: `8`
- current round label: `round 3/10`
- auto use recommended: `yes`
- accepted base run id: `20260419_202711_bf16_gemm_v1_5135c1d`
- accepted base measured commit: `5135c1d6edb580191a96d8c6d9b47cb3ec8b96be`
- accepted base runtime: `30.310320 ms`
- started at: `2026-04-19T20:27:38-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Executing round 3/10.`

## Last completed round

- round: `2/10`
- direction: `dir_01`
- direction name: `Human idea 7/9 Register reuse + Ps2r: move the 64x32 local-half live-set cut onto the true 256x128 hot-band kernel`
- verdict: `regressed`
- runtime delta: `+0.228929 ms`
- TFLOP/s delta: `-0.178569 TFLOP/s`
- run dir: `runs/20260419_204427_bf16_gemm_v1_d777e9e`
- ncu rep path: `runs/20260419_204427_bf16_gemm_v1_d777e9e/ncu_profile.ncu-rep`
