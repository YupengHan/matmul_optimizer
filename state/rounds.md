# Round loop

- active: `yes`
- status: `awaiting_measurement`
- total rounds: `50`
- completed rounds: `15`
- remaining rounds: `35`
- current round label: `round 16/50`
- auto use recommended: `yes`
- accepted base run id: `20260419_222734_bf16_gemm_v1_0d78758`
- accepted base measured commit: `0d787589a75b35984fb169106135c77436806bc6`
- accepted base runtime: `29.325824 ms`
- started at: `2026-04-19T22:34:28-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Build passed for round 16/50. Node A will measure the result next.`

## Last completed round

- round: `15/50`
- direction: `dir_01`
- direction name: `Keep the 128x128/128-thread hot-band branch but revert only the K32 mainloop back to proven K16 staging to localize correctness`
- verdict: `improved`
- runtime delta: `-1.130496 ms`
- TFLOP/s delta: `+0.982491 TFLOP/s`
- run dir: `runs/20260419_233546_bf16_gemm_v1_b42811c`
- ncu rep path: `runs/20260419_233546_bf16_gemm_v1_b42811c/ncu_profile.ncu-rep`
