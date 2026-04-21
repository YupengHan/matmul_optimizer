# Round loop

- active: `yes`
- status: `awaiting_measurement`
- total rounds: `100`
- completed rounds: `5`
- remaining rounds: `95`
- current round label: `round 6/100`
- selection strategy: `frontier_every_5_rounds_else_recommended_v1`
- effective selection mode this round: `frontier`
- auto use recommended: `no`
- auto select frontier: `no`
- accepted base run id: `20260421_105134_bf16_gemm_v1_8dcab81`
- accepted base measured commit: `8dcab81ea44e6d66b1f22c2a768c8e9d3b21223f`
- accepted base runtime: `24.186960 ms`
- started at: `2026-04-21T11:05:50-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Build passed for round 6/100. Node A will measure the result next.`

## Last completed round

- round: `5/100`
- direction: `dir_01`
- direction name: `Re-anchor on the best measured PTX surface under the current workload`
- verdict: `regressed`
- runtime delta: `+0.023039 ms`
- TFLOP/s delta: `-0.007740 TFLOP/s`
- run dir: `runs/20260421_114455_bf16_gemm_v1_aaf076e`
- ncu rep path: `runs/20260421_114455_bf16_gemm_v1_aaf076e/ncu_profile.ncu-rep`
