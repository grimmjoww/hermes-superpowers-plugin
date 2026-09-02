# hermes-superpowers-plugin

> An always-on Superpowers gate for Hermes Agent: procedural discipline is injected automatically instead of depending on the model to remember to request it.

This project adapts [obra/superpowers](https://github.com/obra/superpowers) for [Hermes Agent](https://github.com/NousResearch/hermes-agent) while preserving the upstream skill content and adding the missing enforcement layer.

## The problem it solves

A skill library only helps when the agent actually invokes it. Tool- or MCP-based skill access can still be skipped by a model that rushes into implementation, forgets the procedure, or decides the task is “too simple.”

This plugin moves the rule from an optional tool choice into Hermes' runtime:

- a `pre_llm_call` hook injects the Superpowers rule on the first turn of each session;
- the canonical skills are loaded through Hermes' normal external-skills surface;
- tool names are translated to Hermes-native equivalents with a minimal mapping;
- later turns remain quiet so the plugin does not repeatedly bloat the context.

## What is original here

- the Hermes plugin wrapper;
- the first-turn gate implemented through `pre_llm_call`;
- installation and `skills.external_dirs` wiring;
- the Hermes tool-name compatibility map;
- validation against a live Hermes profile.

The underlying Superpowers skill content comes from `obra/superpowers` and retains its upstream MIT provenance.

## Tool-name mapping

| Canonical name | Hermes surface |
|---|---|
| `Task` | `delegate_task` |
| `Read` | `read_file` |
| `Write` | `write_file` |
| `Edit` | `patch` |
| `Bash` | `terminal` |
| `TodoWrite` | `todo` |
| `Skill` | `skill_view` |

The goal is compatibility, not a rewrite of the upstream methodology.

## Install

```powershell
# Copy the plugin into the Hermes plugin directory
cp -r hermes-superpowers-plugin "$env:HERMES_HOME\plugins\superpowers"
```

Add the skill directory to `config.yaml`:

```yaml
skills:
  external_dirs:
    - "G:\\path\\to\\plugins\\superpowers\\skills"
```

Enable the plugin and restart the Hermes gateway/backend:

```powershell
hermes plugins enable superpowers
```

## Verified behavior

The documented pre-ship checks covered:

1. plugin registration;
2. `pre_llm_call` hook execution;
3. first-turn rule injection;
4. silence on later turns;
5. canonical directory availability through `external_dirs`;
6. `/test-driven-development` resolution;
7. `/systematic-debugging` resolution;
8. `/brainstorming` and `/writing-plans` resolution;
9. no collisions with built-in commands.

**Result: 9/9 checks passing** on the tested Hermes profile.

## Portfolio notes

This repository demonstrates agent-runtime integration rather than prompt writing alone: lifecycle hooks, context discipline, external skill loading, compatibility mapping, collision checks, and explicit behavioral verification.

The plugin wrapper and validation workflow were built through an AI-assisted engineering process directed by **Willie Stewart / Phantom Horizon Studios**. That work included defining the enforcement requirement, separating upstream content from local integration code, directing implementation, reviewing behavior, and requiring named pre-ship checks.

## Provenance

- Skill content: [obra/superpowers](https://github.com/obra/superpowers), MIT, Jesse Vincent
- Compatibility inspiration: [Labhund/hermes-superpowers](https://github.com/Labhund/hermes-superpowers)
- Hermes wrapper, gate, mapping, and verification: this repository

## License

MIT. See `LICENSE.upstream` for upstream attribution.
