# Round loop

- active: `no`
- status: `paused_on_explicit_user_redirect`
- total rounds: `100`
- completed rounds: `10`
- remaining rounds: `90`
- current round label: `single-run`
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
- notes: `Paused on explicit user redirect after round 10/100. Resume from node_b for round 11/100 on latest run 20260421_124420_bf16_gemm_v1_fc400df. Accepted base remains 20260421_105134_bf16_gemm_v1_8dcab81 at 24.186960 ms, and the selection strategy remains frontier_every_5_rounds_else_recommended_v1.`

## Last completed round

- round: `10/100`
- direction: `dir_01`
- direction name: `Retime the PTX barrier seam on the current correctness-safe 128x128 anchor`
- verdict: `improved`
- runtime delta: `-0.136190 ms`
- TFLOP/s delta: `+0.046816 TFLOP/s`
- run dir: `runs/20260421_124420_bf16_gemm_v1_fc400df`
- ncu rep path: `runs/20260421_124420_bf16_gemm_v1_fc400df/ncu_profile.ncu-rep`
