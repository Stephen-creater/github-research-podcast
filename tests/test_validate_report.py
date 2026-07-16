from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "skills" / "github-repo-research" / "scripts" / "validate_report.py"
SPEC = importlib.util.spec_from_file_location("validate_report", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


VALID_REPORT = """# owner/repo: useful project

- 仓库：[owner/repo](https://github.com/owner/repo)
- 本次检查版本：[`abcdef1`](https://github.com/owner/repo/commit/abcdef1234567890)

## 一句话说明

这是一个用于机械测试的仓库研究报告。""" + "有证据的说明。" * 150 + """

## 它解决什么问题

说明问题与用户。

## 怎么安装和使用

说明最小使用路径。

## 架构和重要入口

说明架构，并引用[入口](https://github.com/owner/repo/blob/abcdef1234567890/main.py)。

## 最值得借鉴的设计

说明可复用设计。

## 局限和风险

说明风险和未知项。

## 最终建议

结论是立即使用，并给出最小下一步。

## 主要来源

- [README](https://github.com/owner/repo/blob/abcdef1234567890/README.md)
- [Release](https://github.com/owner/repo/releases/tag/v1.0.0)
"""


class ValidateReportTests(unittest.TestCase):
    def test_valid_report_and_index_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = root / "2026-07-15_owner_repo.md"
            index = root / "index.md"
            report.write_text(VALID_REPORT, encoding="utf-8")
            index.write_text(f"[report]({report.name})\n", encoding="utf-8")
            self.assertEqual([], VALIDATOR.validate(report, index))

    def test_short_unindexed_report_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = root / "bad.md"
            index = root / "index.md"
            report.write_text("# Too short\n", encoding="utf-8")
            index.write_text("# Index\n", encoding="utf-8")
            errors = VALIDATOR.validate(report, index)
            self.assertTrue(any("filename" in error for error in errors))
            self.assertTrue(any("too short" in error for error in errors))
            self.assertTrue(any("does not reference" in error for error in errors))

    def test_secret_signature_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "2026-07-15_owner_repo.md"
            report.write_text(VALID_REPORT + "\nghp_" + "A" * 36, encoding="utf-8")
            errors = VALIDATOR.validate(report)
            self.assertTrue(any("possible secret" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
