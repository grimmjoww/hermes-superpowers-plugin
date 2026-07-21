"""Superpowers for Hermes — always-on skill discipline.

Injects the canonical using-superpowers rule (adapted for Hermes tools) into
the first turn of every session via pre_llm_call. The gates live here, not in
an optional MCP — the agent cannot skip discipline because it never chose it.
"""

_STEERING = """<superpowers>
If you think there is even a 1% chance a skill might apply to what you are doing, you MUST invoke it with `skill_view("<name>")` BEFORE any response or action — including clarifying questions, exploring the codebase, or checking files. This is not negotiable; you cannot rationalize your way out.

- "Let's build X" -> `skill_view("brainstorming")` first, then implementation skills.
- "Fix this bug" -> `skill_view("systematic-debugging")` first, then domain skills.
- Process skills (brainstorming, systematic-debugging) set the approach; implementation skills carry it out.

Skill text written for other platforms maps to Hermes natives on sight: `Task` tool -> `delegate_task`, Read -> `read_file`, Write -> `write_file`, Edit -> `patch`, Bash -> `terminal`, TodoWrite -> `todo`, Skill -> `skill_view`.

Red flags that mean STOP — you are rationalizing: "this is just a simple question", "I need more context first", "let me explore the codebase first", "I remember this skill", "this doesn't count as a task", "the skill is overkill", "I'll just do this one thing first". Check for skills BEFORE doing anything. Then announce "Using [skill] to [purpose]" and follow it exactly; if it has a checklist, make a todo per item.
</superpowers>"""

_fired: set = set()


def register(ctx) -> None:
    ctx.register_hook("pre_llm_call", _pre_llm_call)


def _pre_llm_call(**kwargs):
    try:
        if not kwargs.get("is_first_turn"):
            return None
        sid = kwargs.get("session_id", "")
        if sid in _fired:
            return None
        _fired.add(sid)
        if len(_fired) > 1000:  # bound memory in long-lived gateways
            _fired.clear()
        return _STEERING
    except Exception:
        return None
