# Supervisor context

This file is for the main Codex supervisor. It decides whether to run the next step directly or dispatch a sub-agent.

## Current dispatch

- dispatch node: `node_b`
- dispatch mode: `sub_agent`
- graph status: `ready_for_node_b`
- round label: `round 12/100`
- round loop active: `yes`
- rounds remaining: `89`
- auto-select frontier: `no`
- latest run id: `20260420_233546_bf16_gemm_v1_4bc0218`
- latest runtime: `24.173968 ms`
- recommended direction: `None`
- active direction: `None`

## Supervisor protocol

- read `docs/supervisor_protocol.md` first
- node-specific protocol: `docs/node_b_protocol.md`
- node context file: `state/node_b_context.md`
- prepare command: `python scripts/graph.py node_b`
- finalize command: `python scripts/graph.py node_b --finalize`
- current dispatch requires direct GPU access: `no`

## Dispatch rule

- main agent stays responsible for graph state, commits, and loop control
- spawn exactly one sub-agent for the current node
- after the sub-agent returns, run the finalize command from the main agent
- then re-read `state/supervisor_task.json` before dispatching the next node

## Multi-round loop

- active loop: `round 12/100` with `89` rounds remaining
- auto-use recommended: `yes`
- auto-select frontier: `no`
- context compression cadence: every `5` completed rounds
- last context compression checkpoint: after `10` completed rounds
- next context compression checkpoint: after `15` completed rounds
- keep looping until `state/round_loop_state.json` reports `remaining_rounds = 0` or a failure pauses the loop

## Notes

- `Prepare node_b context if needed, spawn a diagnosis sub-agent, then finalize node_b from the main Codex agent.`
