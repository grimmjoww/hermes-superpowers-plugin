# Superpowers for Hermes Agent

**An always-on Hermes plugin that makes process skills part of the agent's operating environment instead of an optional tool call.**

This project ports the canonical [`obra/superpowers`](https://github.com/obra/superpowers) skill set to [Hermes Agent](https://github.com/NousResearch/hermes-agent) and adds the gate that matters: a `pre_llm_call` hook that injects the skill-first rule on the first turn of every session.

The practical problem is simple. Installing a library of good procedures does not help when the agent forgets to open them. An MCP still leaves discipline as a tool the model must choose. This plugin moves the decision one layer earlier, so the first model call begins with the instruction to check and invoke relevant skills before acting.

## What this repository adds

- **Always-on gate:** the plugin registers a `pre_llm_call` hook with Hermes.
- **First-turn steering:** the hook injects the adapted `using-superpowers` rule at session start.
- **Duplicate protection:** each session ID is tracked so the steering is not repeatedly added on later turns.
- **Bounded runtime state:** the in-memory session set clears after 1,000 entries rather than growing forever.
- **Fail-open behavior:** hook exceptions return `None` instead of taking the Hermes request down.
- **Native skill surface:** the bundled skills load through `skills.external_dirs` and remain callable through `skill_view` and slash commands.
- **Minimal platform adaptation:** upstream skill content is preserved except for the documented Hermes tool-name mapping.

## Architecture

```text
New Hermes session
      ↓
pre_llm_call hook
      ↓
is_first_turn? ── no ──▶ no injection
      │
     yes
      ↓
session already handled? ── yes ──▶ no injection
      │
      no
      ↓
inject skill-first steering into the model context
      ↓
agent selects the relevant Superpowers skill through skill_view
```

The plugin owns the gate. The `skills/` directory supplies the procedures. Hermes continues to own session execution, tool calls, and command routing.

## Included skills

The repository includes 14 skill directories from the upstream Superpowers set:

- brainstorming
- dispatching-parallel-agents
- executing-plans
- finishing-a-development-branch
- receiving-code-review
- requesting-code-review
- subagent-driven-development
- systematic-debugging
- test-driven-development
- using-git-worktrees
- using-superpowers
- verification-before-completion
- writing-plans
- writing-skills

## Hermes tool-name mapping

| Canonical skill text | Hermes surface |
|---|---|
| `Task` | `delegate_task` |
| `Read` | `read_file` |
| `Write` | `write_file` |
| `Edit` | `patch` |
| `Bash` | `terminal` |
| `TodoWrite` | `todo` |
| `Skill` | `skill_view` |

The mapping is intentionally small. The goal is a platform adapter, not a rewrite full of local behavior and project-specific lore.

## Install

Copy the repository into the Hermes plugin directory:

```powershell
Copy-Item -Recurse .\hermes-superpowers-plugin "$env:HERMES_HOME\plugins\superpowers"
```

Add the bundled skills directory to the Hermes configuration:

```yaml
skills:
  external_dirs:
    - "G:\\path\\to\\plugins\\superpowers\\skills"
```

Enable the plugin and restart the Hermes gateway or backend:

```powershell
hermes plugins enable superpowers
```

Use the actual path on your system rather than copying the example drive letter unchanged.

## Verification record

The original build commit records **9/9 pre-ship checks passing on a live Hermes profile**. The checked behaviors were:

1. Plugin registration succeeds.
2. The `pre_llm_call` hook fires.
3. The first turn receives the steering block.
4. Later turns remain silent.
5. The canonical skills directory appears in `external_dirs`.
6. `/test-driven-development` resolves.
7. `/systematic-debugging` resolves.
8. `/brainstorming` and `/writing-plans` resolve.
9. The added commands do not collide with built-in commands.

That result is preserved as a build-time integration record. This repository does not currently contain an automated test suite or CI workflow that independently reruns those nine checks, so the README does not present the number as a continuously verified badge.

## Provenance

- **Skill content:** [`obra/superpowers`](https://github.com/obra/superpowers), MIT, by Jesse Vincent. See [`LICENSE.upstream`](./LICENSE.upstream).
- **Tool-name conversion approach:** independently implemented, informed by [`Labhund/hermes-superpowers`](https://github.com/Labhund/hermes-superpowers).
- **Plugin wrapper, gate, and Hermes adaptation:** this repository, MIT, by `grimmjoww` / Phantom Horizon Studios.

At the time this plugin was built, the missing piece was not access to the written skills; it was an always-on Hermes gate that made consulting them the default behavior.

## Current status

**Version 1.0.0.** Small integration plugin, manually verified on a live Hermes profile at release time.

The wrapper is deliberately compact and readable. Before updating the bundled skills from upstream, compare the current content, preserve the license files, reapply only the documented tool-name mapping, and rerun the first-turn and command-resolution checks.

## Related work

- [Phantom Horizon Studios](https://github.com/grimmjoww/phantom-horizons-studios)
- [Hindsight Installer MCP](https://github.com/grimmjoww/hindsight-installer-mcp)
- [Claude Code + memU](https://github.com/grimmjoww/claude-code-memu)

## License

MIT. Upstream Superpowers content remains attributed under its included license.
