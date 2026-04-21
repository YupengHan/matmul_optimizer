# Supervisor context

This file is for the main Codex supervisor. It decides whether to run the next step directly or dispatch a sub-agent.

## Current dispatch

- dispatch node: `node_a`
- dispatch mode: `direct_script`
- graph status: `ready_for_node_a`
- round label: `round 11/100`
- round loop active: `yes`
- rounds remaining: `90`
- auto-select frontier: `no`
- latest run id: `20260420_233034_bf16_gemm_v1_11df0f1`
- latest runtime: `24.190464 ms`
- recommended direction: `dir_01`
- active direction: `dir_01`

## Supervisor protocol

- read `docs/supervisor_protocol.md` first
- node-specific protocol: `AGENTS.md`
- prepare command: `python scripts/graph.py node_a`
- current dispatch requires direct GPU access: `yes`

## Dispatch rule

- run the script-first node directly from the main agent
- do not spawn a sub-agent for node_a
- after node_a finishes, re-read `state/supervisor_task.json` and continue

## Multi-round loop

- active loop: `round 11/100` with `90` rounds remaining
- auto-use recommended: `yes`
- auto-select frontier: `no`
- context compression cadence: every `5` completed rounds
- last context compression checkpoint: after `10` completed rounds
- next context compression checkpoint: after `15` completed rounds
- keep looping until `state/round_loop_state.json` reports `remaining_rounds = 0` or a failure pauses the loop

## Notes

- `Run node_a directly from the main Codex agent outside the sandbox, then re-read graph state.`
