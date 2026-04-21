# Round loop

- active: `yes`
- status: `running`
- total rounds: `50`
- completed rounds: `14`
- remaining rounds: `36`
- current round label: `round 15/50`
- auto use recommended: `yes`
- accepted base run id: `20260420_185423_bf16_gemm_v1_1181247`
- accepted base measured commit: `1181247a12bfd0978dd155838558142b6386710e`
- accepted base runtime: `24.422464 ms`
- started at: `2026-04-20T17:42:35-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Completed round 14/50. Continue with node_b for round 15/50. Accepted base: 20260420_185423_bf16_gemm_v1_1181247 at 24.422464 ms.`

## Last completed round

- round: `14/50`
- direction: `dir_01`
- direction name: `Activate 128x128x32 Two-K Hot-Band Staging`
- verdict: `regressed`
- runtime delta: `+6.293088 ms`
- TFLOP/s delta: `-5.641652 TFLOP/s`
- run dir: `runs/20260420_194440_bf16_gemm_v1_cb070a7`
- ncu rep path: `runs/20260420_194440_bf16_gemm_v1_cb070a7/ncu_profile.ncu-rep`
