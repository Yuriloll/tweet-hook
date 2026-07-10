# tweet-hook

**Multi-agent skill** for researching viral social openers and generating high-stop-rate tweet/post openings.

Works with **Grok Build, Codex, Claude Code, Cursor, Copilot Chat**, and any agent that can read a `SKILL.md` + markdown references.

---

## What it does

| Feature | Description |
|---------|-------------|
| **Research** | Break down openings from high-engagement posts (when tools allow) |
| **5 hook types** | Contradiction · Anxiety · Topic · Heat · Open loop |
| **Generate** | Paste-ready openers with type / risk / use-case tags |
| **Style transfer** | “Write like @handle” using swipe notes |
| **Offline OK** | L1 mode: local patterns only, no fake “I scraped X” |

### Capability levels

| Level | Meaning |
|-------|---------|
| **L3** | Native X/Twitter search tools |
| **L2** | Web search / fetch URLs |
| **L1** | Local `references/` + user-pasted text only |

The skill **must degrade gracefully**. Missing Grok-only tools is fine.

---

## Repo layout

```
tweet-hook/
  SKILL.md                 # main instructions (all agents)
  INSTALL.md               # install paths per product
  README.md
  references/
    hook-patterns.md       # universal formulas
    list-.../
      swipe-openers.md     # real-world opener swipe
      README.md
      official-pr.md
```

---

## Quick start

```bash
git clone <repo-url> tweet-hook
# see INSTALL.md for Grok / Claude / Codex / Cursor paths
```

Prompt example:

```text
Follow tweet-hook/SKILL.md (L1 if no X tools).
Topic: AI 自媒体接单。Write 12 Chinese openers.
```

---

## Limits

- Cannot export full private following lists  
- Do not invent like/view counts  
- Sample list swipe is a **subset**, not every list member  

---

## License

MIT. Reuse skeletons freely; respect platform rules when quoting others’ full posts.
