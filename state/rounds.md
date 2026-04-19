# Round loop

- active: `yes`
- status: `awaiting_measurement`
- total rounds: `20`
- completed rounds: `19`
- remaining rounds: `1`
- current round label: `round 20/20`
- auto use recommended: `yes`
- accepted base run id: `20260419_013130_bf16_gemm_v1_ea27d5a`
- accepted base measured commit: `ea27d5a906ceb46b0a4ec429d6d53f4a457620d6`
- accepted base runtime: `38.473728 ms`
- started at: `2026-04-18T22:03:53-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Build passed for round 20/20. Node A will measure the result next.`

## Last completed round

- round: `19/20`
- direction: `dir_01`
- direction name: `Keep 64x384, but rework the hot-kernel shared/L1 feed path`
- verdict: `regressed`
- runtime delta: `+0.826879 ms`
- TFLOP/s delta: `-0.397580 TFLOP/s`
- run dir: `runs/20260419_014521_bf16_gemm_v1_4113319`
- ncu rep path: `runs/20260419_014521_bf16_gemm_v1_4113319/ncu_profile.ncu-rep`
