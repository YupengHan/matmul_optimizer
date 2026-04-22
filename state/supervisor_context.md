# Supervisor context

This file is for the main Codex supervisor. It decides whether to run the next step directly or dispatch a sub-agent.

## Current dispatch

- dispatch node: `node_a`
- dispatch mode: `direct_script`
- graph status: `ready_for_node_a`
- round label: `single-run`
- round loop active: `no`
- rounds remaining: `0`
- auto-select frontier: `no`
- latest run id: `20260421_160557_bf16_gemm_v1_35400d35`
- latest runtime: `24.691072 ms`
- recommended direction: `dir_01`
- active direction: `dir_01`
- display update due at current checkpoint: `yes`
- watchdog status: `idle`
- continue required now: `no`
- stop allowed now: `yes`
- natural stop states disallowed: `no`
- interrupt policy: `none`

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

- no multi-round loop is active
- to arm one, run `python scripts/graph.py rounds --count N --auto-use-recommended`

## Watchdog

- timeout: `10` minutes without workflow changes
- latest observed progress: `2026-04-21T17:00:36-07:00` via `state/graph_state.json`
- idle minutes: `N/A`
- watchdog status: `idle`
- continue instruction: `No watchdog action is currently required.`

## Notes

- `Run node_a directly from the main Codex agent outside the sandbox, then re-read graph state.`
