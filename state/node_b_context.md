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
        - `runs/20260421_011816_bf16_gemm_v1_20cad79/summary.json`
        - `runs/20260421_011816_bf16_gemm_v1_20cad79/ncu_metrics.csv`
        - `runs/20260421_011816_bf16_gemm_v1_20cad79/ncu_details.csv`
        - `runs/20260421_011816_bf16_gemm_v1_20cad79/ncu_profile.ncu-rep`

- `state/autotune_round18_main_tiles.json`
- `state/autotune_round18_main_tiles.md`


        Use the raw detailed CSV when the headline summary is too shallow to explain pipeline, memory, or bank-conflict behavior.
        Use the autotune sweep summaries when present to anchor direction ranking in measured tile-width data instead of only one run snapshot.

        ## Output contract

        - write exactly 3 directions
        - preserve `direction_id` values `dir_01`, `dir_02`, `dir_03`
        - keep top-level `family_audit` as a list, even if empty
        - keep top-level `selected_direction_id` as `null` during diagnosis emission unless a later explicit selection writes it
        - each direction must include:
          - `family_id`
          - `subfamily_id`
          - `action_fingerprint`
          - `mode`
          - `hypothesis`
          - `expected_bottleneck`
          - `code_locations`
          - `risk`
          - `metrics_to_recheck`
          - `search_score_v1`
          - `score_breakdown`
          - `predicted_gain_ms`
          - `predicted_fail_risk`
          - `ranking_notes`
        - set `recommended_direction_id`
        - every direction is also treated as a search candidate, so keep numeric score fields and prose notes auditable
        - after editing the diagnosis file, run `python scripts/graph.py node_b --finalize`

        ## Current source snapshot

        - round loop: `round 28/100`
        - rounds remaining after this one: `72`
        - latest run id: `20260421_011816_bf16_gemm_v1_20cad79`
        - median runtime: `24.167423 ms`
        - TFLOP/s: `30.082620 TFLOP/s`
        - measured commit: `20cad7985754ff930f5e7d06a9f6e08152a2635b`
        - existing diagnosis status: `completed`
