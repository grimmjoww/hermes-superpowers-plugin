# Always-On Procedure Enforcement for Hermes Agent

## The Problem

A library of good agent procedures is only useful when the agent actually loads the right procedure before acting. In Hermes, converted Superpowers skills could exist on disk and still remain optional: the model had to remember to call the skill tool before planning, debugging, testing, or editing code.

That created a familiar agent-systems failure. The capability was present, but the behavior needed to activate it was unreliable.

## Design Decision

The solution was to move the requirement outside the model’s voluntary tool choice.

`hermes-superpowers-plugin` adds a Hermes plugin hook that injects the canonical skill-use rule before the first model call in a session. After that first-turn steering, the hook stays silent so it does not repeatedly spend context or interfere with normal conversation.

The design keeps two concerns separate:

- **Canonical skill content** comes from `obra/superpowers`.
- **The Hermes gate, plugin wrapper, and compatibility mapping** live in this repository.

That separation makes the provenance clear and keeps future upstream refreshes manageable.

## Hook Behavior

```text
New Hermes session
      │
      ▼
pre_llm_call hook runs
      │
      ▼
Inject skill-use requirement before first model response
      │
      ▼
Agent loads the relevant skill through Hermes-native tooling
      │
      ▼
Later turns continue without repeated gate injection
```

The hook changes the default from “use a procedure when the model happens to remember” to “begin the session with the procedure requirement already in context.”

## Compatibility Mapping

The plugin preserves the upstream skill bodies except for a narrow tool-name map required by Hermes:

| Canonical surface | Hermes surface |
|---|---|
| `Task` | `delegate_task` |
| `Read` | `read_file` |
| `Write` | `write_file` |
| `Edit` | `patch` |
| `Bash` | `terminal` |
| `TodoWrite` | `todo` |
| `Skill` | `skill_view` |

Keeping the mapping small avoids quietly rewriting the methodology into a different local system.

## Verification

The repository documents nine passing pre-ship checks on the tested Hermes profile:

- plugin registration
- first-turn `pre_llm_call` injection
- silence on later turns
- canonical skill directory registration
- command resolution for test-driven development
- command resolution for systematic debugging
- command resolution for brainstorming
- command resolution for writing plans
- no collisions with built-in commands

The claim is scoped to the tested profile and plugin version. It does not imply that every Hermes configuration has been validated.

## Provenance

- Canonical Superpowers methodology and skill content: `obra/superpowers`, MIT licensed, by Jesse Vincent
- Hermes tool-name adaptation approach: independently implemented, with the repository noting relevant community work
- Plugin wrapper, gate behavior, integration, and verification: this repository under Phantom Horizon Studios

## My Contribution

I identified that merely installing the skills did not make their use dependable, defined the always-on gate requirement, directed the Hermes plugin implementation, constrained the compatibility changes to a minimal tool map, reviewed the repository and test evidence, and verified the integration against a live profile.

The work used an AI-assisted engineering workflow with human control over the design, acceptance criteria, diffs, and verification results.

## Why This Matters to a Client

Many AI systems fail because a capability is technically available but behaviorally optional. This project demonstrates a broader pattern I use in agent work: move critical rules into the system layer, make activation observable, reduce repeated context cost, preserve provenance, and verify the behavior instead of assuming a prompt will be followed.
