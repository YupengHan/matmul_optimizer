        # Node B context

        Node B is the diagnosis node. Read the files below, then write exactly three directions to `state/latest_diagnosis.json`.

        ## Read order

        - `state/latest_run.md`
        - `state/latest_ncu_summary.md`
        - `docs/heuristics.md`
        - `state/progress.md`
        - `state/current_focus.md`
        - `state/human_review.md`
        - `src/kernels/bf16_gemm_v1.cu`
        - `runs/20260420_085928_bf16_gemm_v1_9ee9b48/summary.json`
        - `runs/20260420_085928_bf16_gemm_v1_9ee9b48/ncu_metrics.csv`
        - `runs/20260420_085928_bf16_gemm_v1_9ee9b48/ncu_details.csv`
        - `runs/20260420_085928_bf16_gemm_v1_9ee9b48/ncu_profile.ncu-rep`

- `state/autotune_round18_main_tiles.json`
- `state/autotune_round18_main_tiles.md`


        Use the raw detailed CSV when the headline summary is too shallow to explain pipeline, memory, or bank-conflict behavior.
        Use the autotune sweep summaries when present to anchor direction ranking in measured tile-width data instead of only one run snapshot.

        ## Output contract

        - write exactly 3 directions
        - preserve `direction_id` values `dir_01`, `dir_02`, `dir_03`
        - each direction must include:
          - `hypothesis`
          - `expected_bottleneck`
          - `code_locations`
          - `risk`
          - `metrics_to_recheck`
        - set `recommended_direction_id`
        - after editing the diagnosis file, run `python scripts/graph.py node_b --finalize`

        ## Current source snapshot

        - round loop: `round 61/100`
        - rounds remaining after this one: `39`
        - latest run id: `20260420_085928_bf16_gemm_v1_9ee9b48`
        - median runtime: `25.821696 ms`
        - TFLOP/s: `28.155370 TFLOP/s`
        - measured commit: `9ee9b48dfb73b37b1d93ab38ac84f5dd17f596a2`
        - existing diagnosis status: `completed`
