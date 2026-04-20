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
        - `runs/20260419_171842_bf16_gemm_v1_74f163a/summary.json`
        - `runs/20260419_171842_bf16_gemm_v1_74f163a/ncu_metrics.csv`
        - `runs/20260419_171842_bf16_gemm_v1_74f163a/ncu_details.csv`
        - `runs/20260419_171842_bf16_gemm_v1_74f163a/ncu_profile.ncu-rep`

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

        - round loop: `round 4/20`
        - rounds remaining after this one: `16`
        - latest run id: `20260419_171842_bf16_gemm_v1_74f163a`
        - median runtime: `33.592319 ms`
        - TFLOP/s: `21.642430 TFLOP/s`
        - measured commit: `74f163a73e572099933f7558d0e3413019613a7b`
        - existing diagnosis status: `completed`
