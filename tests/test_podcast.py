from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PODCAST_PATH = ROOT / "skills" / "github-research-podcast" / "scripts" / "podcast.py"
SPEC = importlib.util.spec_from_file_location("podcast", PODCAST_PATH)
assert SPEC and SPEC.loader
PODCAST = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PODCAST
SPEC.loader.exec_module(PODCAST)


class PodcastTests(unittest.TestCase):
    def test_parse_two_speaker_dialogue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "episode.md"
            script.write_text(
                "# Episode\n\n[主持人]\n这个仓库解决什么问题？\n\n"
                "[分析员]\n它把研究结果转换成播客。\n",
                encoding="utf-8",
            )
            turns = PODCAST.parse_dialogue(script)
            self.assertEqual(["主持人", "分析员"], [turn.speaker for turn in turns])

    def test_ignore_markdown_outside_dialogue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "episode.md"
            script.write_text("# Title\n\nThis is metadata only.\n", encoding="utf-8")
            self.assertEqual([], PODCAST.parse_dialogue(script))


if __name__ == "__main__":
    unittest.main()
