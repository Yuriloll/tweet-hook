from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = SKILL_ROOT / "scripts/validate_skill.py"
SPEC = importlib.util.spec_from_file_location("tweet_hook_validator", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load validator from {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateSkillTests(unittest.TestCase):
    def test_current_package_passes(self) -> None:
        self.assertEqual([], VALIDATOR.validate(SKILL_ROOT))

    def test_sample_count_mismatch_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            copied_root = Path(temporary_directory) / "tweet-hook"
            shutil.copytree(SKILL_ROOT, copied_root)
            readme = copied_root / "references/list-2067293665865998356/README.md"
            text = readme.read_text(encoding="utf-8")
            text = text.replace(
                "| @nake13 | Coding agent · 圈内判断 | 10 |",
                "| @nake13 | Coding agent · 圈内判断 | 9 |",
            )
            readme.write_text(text, encoding="utf-8")

            issues = VALIDATOR.validate(copied_root)
            self.assertTrue(
                any("sample count mismatch for @nake13" in issue for issue in issues),
                issues,
            )

    def test_missing_required_file_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            copied_root = Path(temporary_directory) / "tweet-hook"
            shutil.copytree(SKILL_ROOT, copied_root)
            (copied_root / "references/article-hooks.md").unlink()

            issues = VALIDATOR.validate(copied_root)
            self.assertIn(
                "missing required file: references/article-hooks.md",
                issues,
            )


if __name__ == "__main__":
    unittest.main()
