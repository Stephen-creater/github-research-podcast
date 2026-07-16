#!/usr/bin/env python3
"""Compatibility entrypoint for the GitHub Research Podcast CLI."""

from pathlib import Path
import runpy


SCRIPT = Path(__file__).resolve().parent / "skills" / "github-research-podcast" / "scripts" / "podcast.py"
runpy.run_path(str(SCRIPT), run_name="__main__")
