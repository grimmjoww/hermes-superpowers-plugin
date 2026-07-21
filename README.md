# hermes-superpowers-plugin

[obra/superpowers](https://github.com/obra/superpowers) as an **always-on Hermes plugin** — skill discipline you can't skip, because you never chose it.

## Why this exists

Canon superpowers ships as a plugin for Claude Code, Codex, Kimi, and friends — but not for [Hermes Agent](https://github.com/NousResearch/hermes-agent). Community ports (notably [Labhund/hermes-superpowers](https://github.com/Labhund/hermes-superpowers)) converted the skill *content* but left the *gate layer* behind: on those installs, discipline is a tool the agent has to remember to pick up.

An MCP makes discipline **optional**. A plugin makes it **the default state**.

This repo is the missing gate layer, wrapped around canon content:

- **`pre_llm_call` hook** — first turn of every session injects the canonical using-superpowers rule (Hermes-adapted: `skill_view` as the invocation surface). Always on. No choosing.
- **Canon skills** — 14 skills from `obra/superpowers`, converted with a *minimal* Hermes tool-name map and nothing else. No commentary, no local lore baked into skill bodies.
- **Normal Hermes surface** — skills load via `skills.external_dirs`, so `skill_view("test-driven-development")` and `/test-driven-development` work exactly like native skills.

## Install

```powershell
# 1. Copy the plugin into your Hermes home
cp -r hermes-superpowers-plugin "$env:HERMES_HOME\plugins\superpowers"

# 2. Register the skills surface (one line in config.yaml)
#    skills:
#      external_dirs:
#        - "G:\\path\\to\\plugins\\superpowers\\skills"

# 3. Enable the plugin
hermes plugins enable superpowers

# 4. Restart your gateway/backend
```

## The tool-name conversion (all of it)

| Canon says | Hermes native |
|---|---|
| `Task` tool | `delegate_task` |
| `Read` | `read_file` |
| `Write` | `write_file` |
| `Edit` | `patch` |
| `Bash` | `terminal` |
| `TodoWrite` | `todo` |
| `Skill` tool | `skill_view` |

Everything else in the skill bodies is byte-identical to upstream canon. If a future upstream release changes content, re-copy `skills/` from a fresh clone and re-apply this table.

## Verified

Built test-first on a live Hermes profile. The pre-ship checks: plugin registers, `pre_llm_call` hook fires, first turn injects steering, later turns stay silent, canon dir appears in `external_dirs`, `/test-driven-development` `/systematic-debugging` `/brainstorming` `/writing-plans` resolve as commands, zero collisions with built-in commands. **9/9 passing.**

## Provenance

- Skill content: [obra/superpowers](https://github.com/obra/superpowers) (MIT, Jesse Vincent) — see `LICENSE.upstream`
- Tool-name conversion approach: independent, informed by [Labhund/hermes-superpowers](https://github.com/Labhund/hermes-superpowers)
- Plugin wrapper + gates: this repo (MIT, grimmjoww / Phantom Horizon Studios)

Built with [Hermes Agent](https://github.com/NousResearch/hermes-agent).
