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
        - `runs/20260420_193817_bf16_gemm_v1_0a37b0b/summary.json`
        - `runs/20260420_193817_bf16_gemm_v1_0a37b0b/ncu_metrics.csv`
        - `runs/20260420_193817_bf16_gemm_v1_0a37b0b/ncu_details.csv`
        - `runs/20260420_193817_bf16_gemm_v1_0a37b0b/ncu_profile.ncu-rep`

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

        - round loop: `round 14/50`
        - rounds remaining after this one: `36`
        - latest run id: `20260420_193817_bf16_gemm_v1_0a37b0b`
        - median runtime: `25.504256 ms`
        - TFLOP/s: `28.505808 TFLOP/s`
        - measured commit: `0a37b0bf9d796f268c056ce6bbdb5424f9f7e25f`
        - existing diagnosis status: `completed`
