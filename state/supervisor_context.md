# Supervisor context

This file is for the main Codex supervisor. It decides whether to run the next step directly or dispatch a sub-agent.

## Current dispatch

- dispatch node: `node_a`
- dispatch mode: `direct_script`
- graph status: `ready_for_node_a`
- round label: `single-run`
- round loop active: `no`
- rounds remaining: `0`
- latest run id: `20260418_195405_bf16_gemm_v1_a4966f5`
- latest runtime: `298.095123 ms`
- recommended direction: `dir_01`
- active direction: `dir_01`

## Supervisor protocol

- read `docs/supervisor_protocol.md` first
- node-specific protocol: `AGENTS.md`
- prepare command: `python scripts/graph.py node_a`
- node_a requires direct GPU access: `yes`

## Dispatch rule

- run the script-first node directly from the main agent
- do not spawn a sub-agent for node_a
- after node_a finishes, re-read `state/supervisor_task.json` and continue

## Multi-round loop

- no multi-round loop is active
- to arm one, run `python scripts/graph.py rounds --count N --auto-use-recommended`

## Notes

- `Run node_a directly from the main Codex agent outside the sandbox, then re-read graph state.`
