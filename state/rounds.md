# Round loop

- active: `yes`
- status: `running`
- total rounds: `5`
- completed rounds: `3`
- remaining rounds: `2`
- current round label: `round 4/5`
- auto use recommended: `no`
- accepted base run id: `20260419_122438_bf16_gemm_v1_15d63b2`
- accepted base measured commit: `15d63b2993c6eecc3a912dc4a648de6294e82efc`
- accepted base runtime: `35.725824 ms`
- started at: `2026-04-19T12:25:01-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Completed round 3/5. Continue with node_b for round 4/5. Accepted base: 20260419_122438_bf16_gemm_v1_15d63b2 at 35.725824 ms.`

## Last completed round

- round: `3/5`
- direction: `dir_01`
- direction name: `Straight-line the Tile384 cp.async producer schedule on the restored base`
- verdict: `regressed`
- runtime delta: `+5.092001 ms`
- TFLOP/s delta: `-2.443260 TFLOP/s`
- run dir: `runs/20260419_124436_bf16_gemm_v1_05bac60`
- ncu rep path: `runs/20260419_124436_bf16_gemm_v1_05bac60/ncu_profile.ncu-rep`
