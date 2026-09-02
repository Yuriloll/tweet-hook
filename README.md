# tweet-hook

Evidence-grounded, cross-agent skill for researching social openers and generating high-stop-rate tweet/post openings.

Works with **Grok Build, Codex, Claude Code, Cursor, Copilot Chat**, and any agent that can read a `SKILL.md` + markdown references.

“Cross-agent” means portable across these environments. The workflow does not require or claim parallel multi-agent execution.

---

## What it does

| Feature | Description |
|---------|-------------|
| **Research** | Break down openings from high-engagement posts (when tools allow) |
| **Hook Brief** | Identify reader · pain · counterintuitive point · number/result · curiosity line before drafting |
| **5 hook types** | Contradiction · Anxiety · Topic · Heat · Curiosity/open loop |
| **Generate** | Paste-ready openers with type / risk / use-case tags |
| **Style adaptation** | Reuse structural patterns and rhythm without copying distinctive wording |
| **Offline OK** | L1 mode: local patterns only, no fake “I scraped X” |
| **Validation** | Check package structure, references, naming, and swipe-count consistency |

### Capability levels

| Level | Meaning |
|-------|---------|
| **L3** | Native X/Twitter search tools |
| **L2** | Web search / fetch URLs |
| **L1** | Local `references/` + user-pasted text only |

The skill **must degrade gracefully**. Missing Grok-only tools is fine.

Capability level describes available tools; run mode describes what was actually used. An L2/L3 agent using only user material should report both facts instead of calling the environment L1.

---

## Repo layout

```
tweet-hook/
  SKILL.md                 # main instructions (all agents)
  INSTALL.md               # install paths per product
  README.md
  AGENTS.md                # lightweight loader instructions
  scripts/
    validate_skill.py      # deterministic package checks
  tests/
    test_validate_skill.py
  references/
    hook-patterns.md       # universal formulas
    article-hooks.md       # long-form/tutorial opener patterns
    list-.../
      swipe-openers.md     # real-world opener swipe
      README.md
      official-pr.md
```

---

## Quick start

```bash
git clone https://github.com/Yuriloll/tweet-hook.git
# see INSTALL.md for Grok / Claude / Codex / Cursor paths
```

Prompt example:

```text
Follow tweet-hook/SKILL.md (L1 if no X tools).
Topic: AI 自媒体接单。先完成 Hook Brief，再写 12 个中文开头。
```

The mandatory pre-draft sequence is:

`reader → current pain → counterintuitive point → concrete number/result → strongest curiosity line → hook type → draft → payoff sentence`

Missing evidence stays missing. The skill must not invent a number, observation, test, causal claim, or impact to fill a template.

---

## Limits

- Cannot export full private following lists  
- Do not invent like/view counts  
- Sample list swipe is a **subset**, not every list member  
- Historical engagement values are snapshots, not current claims

---

## Validate

```bash
python3 scripts/validate_skill.py .
python3 -m unittest discover -s tests -v
```

These checks validate the package and sample bookkeeping. Rhetorical quality still requires a realistic input review using the quality bar in `SKILL.md`.

---

## License

MIT. Reuse skeletons freely; respect platform rules when quoting others’ full posts.
