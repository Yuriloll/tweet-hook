#!/usr/bin/env python3
"""Validate tweet-hook package structure and sample bookkeeping."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

REQUIRED_FILES = (
    "SKILL.md",
    "AGENTS.md",
    "README.md",
    "INSTALL.md",
    "references/hook-patterns.md",
    "references/priority-templates.md",
    "references/creator-styles.md",
    "references/emotional-openers.md",
    "references/research-2026-09.md",
    "references/research-2026-09.json",
    "references/article-hooks.md",
    "references/list-2067293665865998356/README.md",
    "references/list-2067293665865998356/swipe-openers.md",
    "references/list-2067293665865998356/official-pr.md",
    "scripts/validate_skill.py",
    "tests/test_validate_skill.py",
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

def check_research(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        data = json.loads(read_text(path))
        index, curated, counts = data["index"], data["curated"], data["collection"]
        first = date.fromisoformat(data["requested_window"]["since"])
        last = date.fromisoformat(data["requested_window"]["through"])
        ids = [row["id"] for row in index]
        selected_ids = [row["id"] for row in curated]
        if len(ids) != len(set(ids)) or len(selected_ids) != len(set(selected_ids)):
            issues.append("duplicate research source IDs")
        by_id = {row["id"]: row for row in index}
        handles = dict(Counter(row["handle"] for row in index))
        months = {handle: dict(Counter(row["date"][:7] for row in index
                                      if row["handle"] == handle)) for handle in handles}
        computed = {
            "unique": len(index), "curated": len(curated),
            "text_available": sum(row["text_available"] for row in index),
            "browser_unique": sum("X browser Top search" in row["sources"] for row in index),
            "api_returned": sum("6551 API" in row["sources"] for row in index),
            "by_handle": handles, "by_month": months,
        }
        for key, value in computed.items():
            if counts.get(key) != value:
                issues.append(f"research count mismatch: {key}")
        for row in index:
            sid = row["id"]
            if not re.fullmatch(r"\d+", sid):
                issues.append(f"invalid research ID: {sid}")
            if row["url"] != f"https://x.com/{row['handle']}/status/{sid}":
                issues.append(f"research URL identity mismatch: {sid}")
            if not first <= date.fromisoformat(row["date"]) <= last:
                issues.append(f"research date outside window: {sid}")
            if type(row["text_available"]) is not bool or not row["sources"]:
                issues.append(f"research source metadata incomplete: {sid}")
            if row["metrics"] is not None:
                if not row.get("metrics_observed_on"):
                    issues.append(f"metrics missing observation date: {sid}")
                if any(type(value) is not int or value < 0 for value in row["metrics"].values()):
                    issues.append(f"invalid metrics: {sid}")
            elif not row.get("metrics_note"):
                issues.append(f"missing metrics explanation: {sid}")
        for row in curated:
            sid = row["id"]
            source = by_id.get(sid)
            if source is None:
                issues.append(f"curated source missing from index: {sid}")
                continue
            if not source["text_available"]:
                issues.append(f"curated source has no observed text: {sid}")
            for field in ("handle", "date", "url", "sources", "metrics"):
                if row[field] != source[field]:
                    issues.append(f"curated source mismatch: {sid} {field}")
            if not 0 < len(row["excerpt"]) <= 24:
                issues.append(f"excerpt must be a short nonempty quote: {sid}")
            if not all(row.get(field) for field in ("mechanism", "analysis", "caveat")):
                issues.append(f"curated analysis incomplete: {sid}")
    except (KeyError, TypeError, ValueError) as exc:
        issues.append(f"invalid research data: {exc}")
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

    research_path = root / "references/research-2026-09.json"
    if research_path.is_file():
        issues.extend(check_research(research_path))
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
    research = json.loads(read_text(root / "references/research-2026-09.json"))
    print(f"tweet-hook validation passed ({sample_total} legacy rows; "
          f"{len(research['index'])} research IDs; {len(research['curated'])} source cards)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
