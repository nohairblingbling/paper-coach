from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "paper-coach" / "scripts" / "build_paper_map.py"
SPEC = importlib.util.spec_from_file_location("build_paper_map", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BuildPaperMapTests(unittest.TestCase):
    def test_normalize_handles_markdown_and_unicode(self) -> None:
        self.assertEqual(MODULE.normalize("**Figure １:**  Dense   Block"), "figure 1 dense block")
        self.assertEqual(MODULE.normalize("### 摘要"), "摘要")

    def test_find_page_is_one_indexed(self) -> None:
        pages = [
            "Title and Abstract on the first page",
            "Figure 2: Architecture of the proposed method",
        ]
        self.assertEqual(MODULE.find_page("Abstract", pages), 1)
        self.assertEqual(MODULE.find_page("Figure 2: Architecture", pages), 2)
        self.assertIsNone(MODULE.find_page("Not present", pages))

    def test_caption_regex_is_multilingual(self) -> None:
        samples = ["**Figure 1:** Model", "Table 2: Results", "图 3：架构", "表 4：结果", "図 5: 概要"]
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertIsNotNone(MODULE.CAPTION_RE.match(sample))

    def test_find_miyo_uses_path_fallback(self) -> None:
        with patch.object(MODULE.Path, "exists", return_value=False), patch.object(
            MODULE.shutil, "which", side_effect=lambda name: "/usr/bin/miyo" if name == "miyo" else None
        ):
            self.assertEqual(MODULE.find_miyo(), "/usr/bin/miyo")


if __name__ == "__main__":
    unittest.main()
