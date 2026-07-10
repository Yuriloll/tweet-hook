# Install tweet-hook on any AI agent

This skill is **tool-agnostic**. Core value lives in:

- `SKILL.md` — procedures
- `references/` — patterns + swipe library

## Universal install

```bash
git clone <your-repo-url> tweet-hook
# then copy into the agent path you use (examples below)
```

Or download ZIP from GitHub → extract → copy folder.

---

## Grok Build

**User-wide:**

```bash
mkdir -p ~/.grok/skills/tweet-hook
cp -R tweet-hook/* ~/.grok/skills/tweet-hook/
```

**Project:**

```bash
mkdir -p .grok/skills/tweet-hook
cp -R tweet-hook/* .grok/skills/tweet-hook/
```

Invoke: `/tweet-hook` or natural language（推文开头 / 爆款钩子）.

---

## Claude Code

```bash
mkdir -p .claude/skills/tweet-hook
cp -R tweet-hook/* .claude/skills/tweet-hook/
```

Or user skills directory if you use one.  
Invoke by skill name or: “Follow .claude/skills/tweet-hook/SKILL.md”.

---

## OpenAI Codex (CLI / IDE)

```bash
mkdir -p .agents/skills/tweet-hook   # or your project skills path
cp -R tweet-hook/* .agents/skills/tweet-hook/
```

Also works if you add to `AGENTS.md`:

```markdown
When writing tweet/X openers, follow ./path/to/tweet-hook/SKILL.md
and use references/ under that skill.
```

In chat you can `@tweet-hook/SKILL.md` if the product supports file refs.

---

## Cursor

```bash
mkdir -p .cursor/skills/tweet-hook
cp -R tweet-hook/* .cursor/skills/tweet-hook/
```

Or Project Rules → point to `SKILL.md`.

---

## GitHub Copilot Chat / other

1. Keep this folder in the repo.  
2. In the system or custom instruction:

```text
For viral tweet openings, follow skills/tweet-hook/SKILL.md.
Prefer references/hook-patterns.md and references/**/swipe-openers.md.
If you cannot search X, use L1 offline mode only.
```

---

## Verify

Ask the agent:

```text
Read tweet-hook SKILL.md and say your capability level L1/L2/L3,
then write 5 openers for: "AI 工作流接单"
```

Expected:

- States L1/L2/L3  
- Uses hook types  
- Outputs paste-ready openers without inventing fake metrics  
