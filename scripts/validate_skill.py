#!/usr/bin/env python3
"""Validate tweet-hook package structure and sample bookkeeping."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_FILES = (
    "SKILL.md",
    "AGENTS.md",
    "README.md",
    "INSTALL.md",
    "references/hook-patterns.md",
    "references/article-hooks.md",
    "references/list-2067293665865998356/README.md",
    "references/list-2067293665865998356/swipe-openers.md",
    "references/list-2067293665865998356/official-pr.md",
    "scripts/validate_skill.py",
    "tests/test_validate_skill.py",
)

REQUIRED_SKILL_PHRASES = (
    "## 5. Hook mining workflow（生成前置诊断）",
    "判断读者是谁",
    "判断读者现在最痛的点",
    "提取内容里最反常识的观点",
    "找出最具体的数字或结果",
    "判断哪句话最容易制造好奇心",
    "能力级别表示环境",
    "本轮模式表示",
    "默认必须展示 `Hook Brief`",
    "已核实",
    "用户提供",
    "推断",
    "缺失",
    "好奇（信息缺口）",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_frontmatter(skill_text: str) -> list[str]:
    issues: list[str] = []
    if not skill_text.startswith("---\n"):
        return ["SKILL.md must start with YAML frontmatter"]

    parts = skill_text.split("---", 2)
    if len(parts) < 3:
        return ["SKILL.md frontmatter is not closed"]

    frontmatter = parts[1]
    if not re.search(r"(?m)^name:\s*tweet-hook\s*$", frontmatter):
        issues.append("SKILL.md frontmatter name must be tweet-hook")
    if not re.search(r"(?m)^description:\s*(?:>|\S)", frontmatter):
        issues.append("SKILL.md frontmatter requires a description")
    return issues


def declared_sample_counts(readme_text: str) -> tuple[dict[str, int], int | None]:
    counts: dict[str, int] = {}
    row_pattern = re.compile(
        r"^\|\s*(@[A-Za-z0-9_]+)\s*\|.*\|\s*(\d+)\s*\|\s*$"
    )
    for line in readme_text.splitlines():
        match = row_pattern.match(line)
        if match:
            counts[match.group(1)] = int(match.group(2))

    total_match = re.search(r"当前表格记录数:\*\*\s*(\d+)", readme_text)
    total = int(total_match.group(1)) if total_match else None
    return counts, total


def actual_sample_counts(swipe_text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    current_handle: str | None = None
    data_row = re.compile(r"^\|\s*\d[\d,]*\+?\s*\|")

    for line in swipe_text.splitlines():
        if line.startswith("# 跨账号"):
            break
        heading = re.match(r"^##\s+(@[A-Za-z0-9_]+)", line)
        if heading:
            current_handle = heading.group(1)
            counts.setdefault(current_handle, 0)
            continue
        if current_handle and data_row.match(line):
            counts[current_handle] += 1
    return counts


def check_markdown_links(root: Path) -> list[str]:
    issues: list[str] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for markdown_file in root.rglob("*.md"):
        for raw_target in link_pattern.findall(read_text(markdown_file)):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            if not (markdown_file.parent / target).resolve().exists():
                relative_file = markdown_file.relative_to(root)
                issues.append(f"broken local link in {relative_file}: {raw_target}")
    return issues


def validate(root: Path) -> list[str]:
    root = root.resolve()
    issues: list[str] = []

    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).is_file():
            issues.append(f"missing required file: {relative_path}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill_text = read_text(skill_path)
        issues.extend(check_frontmatter(skill_text))
        for phrase in REQUIRED_SKILL_PHRASES:
            if phrase not in skill_text:
                issues.append(f"SKILL.md missing required workflow phrase: {phrase}")
        if "矛盾 / 焦虑 / 话题 / 热度 / 钩子" in skill_text:
            issues.append("SKILL.md still uses the ambiguous fifth category name 钩子")
        if "可用「据我观察 / 我们测下来」" in skill_text:
            issues.append("SKILL.md still permits unsupported observation/test claims")
        if re.search(r"(?i)multi-agent skill", skill_text):
            issues.append("SKILL.md still claims to be a multi-agent skill")

    list_readme = root / "references/list-2067293665865998356/README.md"
    swipe_file = root / "references/list-2067293665865998356/swipe-openers.md"
    if list_readme.is_file() and swipe_file.is_file():
        declared, declared_total = declared_sample_counts(read_text(list_readme))
        actual = actual_sample_counts(read_text(swipe_file))
        for handle in sorted(set(declared) | set(actual)):
            if declared.get(handle) != actual.get(handle):
                issues.append(
                    f"sample count mismatch for {handle}: "
                    f"README={declared.get(handle)}, swipe={actual.get(handle)}"
                )
        actual_total = sum(actual.values())
        if declared_total is None:
            issues.append("sample README must declare 当前表格记录数")
        elif declared_total != actual_total:
            issues.append(
                f"sample total mismatch: README={declared_total}, swipe={actual_total}"
            )

    issues.extend(check_markdown_links(root))
    return issues


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[1]
    issues = validate(root)
    if issues:
        print("tweet-hook validation failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    swipe_text = read_text(
        root / "references/list-2067293665865998356/swipe-openers.md"
    )
    sample_total = sum(actual_sample_counts(swipe_text).values())
    print(f"tweet-hook validation passed ({sample_total} swipe rows checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
