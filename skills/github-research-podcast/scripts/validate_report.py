#!/usr/bin/env python3
"""Validate the mechanical quality contract for one repository research report."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_[A-Za-z0-9_.-]+_[A-Za-z0-9_.-]+\.md$")
GITHUB_LINK_RE = re.compile(r"https://github\.com/[^\s)]+")
REVISION_RE = re.compile(r"\b[0-9a-f]{7,40}\b", re.IGNORECASE)
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"\b(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
}

REQUIRED_SECTIONS = {
    "plain explanation": ("一句话", "one-sentence"),
    "problem": ("解决什么问题", "problem"),
    "usage": ("安装和使用", "怎么使用", "setup", "minimal use"),
    "architecture": ("架构", "architecture"),
    "reusable ideas": ("值得借鉴", "可复用", "reusable"),
    "recent project help": ("近期项目", "直接帮助", "对我们有什么", "project help", "recent projects"),
    "risks": ("局限", "风险", "limitations", "risks"),
    "recommendation": ("最终建议", "建议", "recommendation"),
    "sources": ("主要来源", "一手来源", "primary sources"),
}


def section_headings(text: str) -> list[str]:
    return [line.lstrip("#").strip().lower() for line in text.splitlines() if line.startswith("## ")]


def validate(report: Path, index: Path | None = None) -> list[str]:
    errors: list[str] = []
    if not report.is_file():
        return [f"report does not exist: {report}"]

    text = report.read_text(encoding="utf-8")
    headings = section_headings(text)

    if not FILENAME_RE.fullmatch(report.name):
        errors.append("filename must match YYYY-MM-DD_owner_repo.md")
    if len(text.strip()) < 1200:
        errors.append("report is too short; expected at least 1200 characters")
    if not text.startswith("# "):
        errors.append("report must begin with one H1 title")

    for label, aliases in REQUIRED_SECTIONS.items():
        if not any(any(alias in heading for alias in aliases) for heading in headings):
            errors.append(f"missing section: {label}")

    links = GITHUB_LINK_RE.findall(text)
    if len(set(links)) < 3:
        errors.append("include at least three distinct GitHub primary-source links")
    if not REVISION_RE.search(text):
        errors.append("include the exact inspected commit revision (7-40 hex characters)")

    recommendation_terms = ("立即使用", "现在就", "仅研究", "研究为主", "跳过", "use now", "study only", "skip")
    if not any(term in text.lower() for term in recommendation_terms):
        errors.append("recommendation must clearly choose Use now, Study only, or Skip")

    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"possible secret detected: {label}")

    if index is not None:
        if not index.is_file():
            errors.append(f"index does not exist: {index}")
        elif report.name not in index.read_text(encoding="utf-8"):
            errors.append(f"index does not reference {report.name}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--index", type=Path)
    args = parser.parse_args()

    errors = validate(args.report, args.index)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
