        # Node B context

        Node B is the diagnosis node. Read the files below, then write exactly three directions to `state/latest_diagnosis.json`.
        Prioritize the structured bottleneck / hotspot / delta handoff first. Only fall back to raw CSV or `.ncu-rep` when the structured summary is insufficient.

        ## Read order

        - `state/node_b_context.md`
        - `state/latest_run.md`
        - `state/latest_ncu_summary.md`
        - `runs/20260421_145629_bf16_gemm_v1_5383596d/ncu_analysis.md`
        - `runs/20260421_145629_bf16_gemm_v1_5383596d/ncu_analysis.json`
        - `docs/heuristics.md`
        - `state/progress.md`
        - `state/current_focus.md`
        - `state/human_review.md`
        - `src/kernels/bf16_gemm_v1.cu`
        - `runs/20260421_145629_bf16_gemm_v1_5383596d/summary.json`
        - `runs/20260421_145629_bf16_gemm_v1_5383596d/ncu_details_page.csv`
        - `runs/20260421_145629_bf16_gemm_v1_5383596d/ncu_source.csv`
        - `runs/20260421_145629_bf16_gemm_v1_5383596d/ncu_import_raw.csv`
        - `runs/20260421_145629_bf16_gemm_v1_5383596d/ncu_details.csv`
        - `runs/20260421_145629_bf16_gemm_v1_5383596d/ncu_metrics.csv`
        - `runs/20260421_145629_bf16_gemm_v1_5383596d/ncu_profile.ncu-rep`

- `state/autotune_round18_main_tiles.json`
- `state/autotune_round18_main_tiles.md`


        ## Optional cuBLAS reference

        If the latest custom run does not suggest a clear next move, inspect the cuBLAS reference artifacts below to see how much hardware utilization the vendor library reaches on the same data.

- `runs/20260421_133046_cublas_ref_v4_lt_best/ncu_analysis.md`
- `runs/20260421_133046_cublas_ref_v4_lt_best/ncu_analysis.json`
- `runs/20260421_133046_cublas_ref_v4_lt_best/ncu_summary.json`
- `runs/20260421_133046_cublas_ref_v4_lt_best/ncu_profile.ncu-rep`

        Use the structured summary first:
        - `bottleneck_classes` tells you which bottleneck family is currently dominant
        - `top_findings` tells you which section, rule, hotspot, or delta is most actionable
        - `top_source_hotspots` and `handoff.node_c.target_hotspots` tell you where local hardware pressure concentrates
        - `delta_vs_previous_run` tells you what changed after the last code edit
        Use the raw exports only when the structured findings are not enough to explain pipeline, memory, synchronization, or source-level behavior.
        Use the autotune sweep summaries when present to anchor direction ranking in measured tile-width data instead of only one run snapshot.

        ## Output contract

        - write exactly 3 directions
        - preserve `direction_id` values `dir_01`, `dir_02`, `dir_03`
        - keep top-level `family_audit` as a list
        - keep top-level `selected_direction_id` as `null` during diagnosis emission unless a later explicit selection writes it
        - set `reasoning_source` to `main_codex_agent` or `codex_sub_agent`
        - set `reasoning_mode` to `manual_reasoned_best_model`
        - write a non-empty `reasoning_summary` with concrete ranking rationale
        - write `evidence_refs` as a non-empty list of concrete files reviewed
        - the diagnosis must come from live reasoning, not from a repo-external scripted helper
        - all 3 direction `name` fields must be distinct
        - all 3 direction `action_fingerprint` values must be distinct
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
        - each direction may additionally include:
          - `evidence_refs`
          - `target_hotspots`
          - `expected_local_changes`
          - `guardrail_metrics`
        - set `recommended_direction_id`
        - every direction is also treated as a search candidate, so keep numeric score fields and prose notes auditable
        - after editing the diagnosis file, run `python scripts/graph.py node_b --finalize`

        ## Current source snapshot

        - round loop: `round 3/10`
        - rounds remaining after this one: `7`
        - latest run id: `20260421_145629_bf16_gemm_v1_5383596d`
        - median runtime: `47.290880 ms`
        - TFLOP/s: `15.373354 TFLOP/s`
        - measured commit: `5383596d7276d7daebbe92c3dc04bea84a505aac`
        - existing diagnosis status: `completed`
        - top bottleneck class: `occupancy_latency_hiding_issue`
        - top finding: `Launch Statistics is carrying metric Registers Per Thread.`
