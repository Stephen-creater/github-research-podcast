#!/usr/bin/env python3
"""Install the bundled github-research-podcast Skill into an Agent skill root."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "skills" / "github-research-podcast"


def directories_match(left: Path, right: Path) -> bool:
    comparison = filecmp.dircmp(left, right)
    if comparison.left_only or comparison.right_only or comparison.funny_files:
        return False
    if comparison.diff_files:
        return False
    return all(directories_match(left / name, right / name) for name in comparison.common_dirs)


def install(target_root: Path, force: bool) -> tuple[Path, str]:
    if not (SOURCE / "SKILL.md").is_file():
        raise RuntimeError(f"bundled Skill is incomplete: {SOURCE}")

    destination = target_root.expanduser().resolve() / SOURCE.name
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        if directories_match(SOURCE, destination):
            return destination, "already up to date"
        if not force:
            raise RuntimeError(
                f"destination exists and differs: {destination}\n"
                "Review it first, then rerun with --force to replace it."
            )
        if destination.is_dir():
            shutil.rmtree(destination)
        else:
            destination.unlink()

    shutil.copytree(SOURCE, destination)
    return destination, "installed"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target-root",
        type=Path,
        default=Path.home() / ".codex" / "skills",
        help="Agent skill root (default: ~/.codex/skills)",
    )
    parser.add_argument("--force", action="store_true", help="replace a differing installation")
    args = parser.parse_args()

    try:
        destination, status = install(args.target_root, args.force)
    except (OSError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"{status}: {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
