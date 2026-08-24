from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "paper-coach" / "SKILL.md"


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SKILL.read_text(encoding="utf-8")

    def test_repo_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_repo.py")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_one_answer_opportunity_is_explicit(self) -> None:
        self.assertIn("One answer opportunity per checkpoint", self.text)
        self.assertIn("Never use future-stage evidence", self.text)
        self.assertIn("The question itself must not introduce", self.text)

    def test_quick_questions_are_present(self) -> None:
        questions = [
            "What did the authors try to accomplish?",
            "What were the key elements of the approach?",
            "What can you use yourself?",
            "What other references do you want to follow?",
        ]
        for question in questions:
            with self.subTest(question=question):
                self.assertIn(question, self.text)

    def test_registry_visible_attribution_is_prominent(self) -> None:
        attribution = "## Origin and Attribution"
        when_to_use = "## When to Use"
        self.assertIn(attribution, self.text)
        self.assertLess(self.text.index(attribution), self.text.index(when_to_use))
        self.assertIn("Andrew Ng (吴恩达)", self.text)
        self.assertIn("https://www.youtube.com/watch?v=733m6qBH-jI", self.text)
        self.assertIn("independent extensions", self.text)

    def test_removed_disclaimer_is_absent_from_current_docs(self) -> None:
        current_docs = [
            SKILL,
            ROOT / "README.md",
            ROOT / "skills" / "paper-coach" / "references" / "andrew-ng-method.md",
        ]
        forbidden = [
            "not affiliated with, sponsored by, or endorsed by",
            "不存在隶属、赞助或背书关系",
        ]
        for path in current_docs:
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden:
                with self.subTest(path=path, phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_no_machine_local_path_in_skill_bundle(self) -> None:
        for path in (ROOT / "skills" / "paper-coach").rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".py", ".txt"}:
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(re.search(r"/Users/[^/\s]+/|/home/[^/\s]+/", text), str(path))


if __name__ == "__main__":
    unittest.main()
