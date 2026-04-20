# Round loop

- active: `yes`
- status: `awaiting_measurement`
- total rounds: `100`
- completed rounds: `33`
- remaining rounds: `67`
- current round label: `round 34/100`
- auto use recommended: `yes`
- accepted base run id: `20260420_002759_bf16_gemm_v1_1b9dbe3`
- accepted base measured commit: `1b9dbe3d306090b4f1762f1e1a504c13d2ab5d92`
- accepted base runtime: `26.924031 ms`
- started at: `2026-04-19T22:34:28-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Build passed for round 34/100. Node A will measure the result next.`

## Last completed round

- round: `33/100`
- direction: `dir_01`
- direction name: `Rewrite the active 128x128 K16 hot-band steady-state around Pg2s/Stage orchestration instead of dead grouped_rows tuning`
- verdict: `regressed`
- runtime delta: `+4.553823 ms`
- TFLOP/s delta: `-3.851337 TFLOP/s`
- run dir: `runs/20260420_004325_bf16_gemm_v1_bbb7383`
- ncu rep path: `runs/20260420_004325_bf16_gemm_v1_bbb7383/ncu_profile.ncu-rep`
