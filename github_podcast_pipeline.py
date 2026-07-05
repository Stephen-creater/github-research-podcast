#!/usr/bin/env python3
"""Small local pipeline for GitHub-to-podcast experiments.

This intentionally avoids paid APIs. It can clone/update selected repos, produce
lightweight repo briefs, and synthesize a marked-up Chinese dialogue script with
macOS `say` plus `ffmpeg`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORK_REPOS = ROOT / "work" / "repos"
OUTPUTS = ROOT / "outputs"


DEFAULT_REPOS = [
    {
        "name": "gitingest",
        "url": "https://github.com/coderamp-labs/gitingest.git",
        "role": "Turn a Git repository into prompt-friendly LLM context.",
    },
    {
        "name": "Audicle",
        "url": "https://github.com/ttlequals0/Audicle.git",
        "role": "Turn saved articles and documents into a private podcast feed.",
    },
    {
        "name": "ai-podcast-studio",
        "url": "https://github.com/sourcelabs-nl/ai-podcast-studio.git",
        "role": "Monitor sources, score relevance, compose scripts, synthesize audio, and publish RSS.",
    },
    {
        "name": "feishu-pm-kit",
        "url": "https://github.com/Winfred1024/feishu-pm-kit.git",
        "role": "Productized Feishu project-manager agent built around Claude Code and Lark CLI.",
    },
    {
        "name": "feishu-claude-code",
        "url": "https://github.com/H2O-YAOZE/feishu-claude-code.git",
        "role": "Use Feishu as a remote control for Claude Code running on the user's computer.",
    },
    {
        "name": "Morning-news-podcast",
        "url": "https://github.com/niuz3199-collab/Morning-news-podcast.git",
        "role": "Android daily news audio briefing with LLM script generation and TTS.",
    },
]


VOICE_MAP = {
    "主持人": "Tingting",
    "分析员": "Reed (Chinese (China mainland))",
    "旁白": "Tingting",
}


@dataclass
class DialogueTurn:
    speaker: str
    text: str


def run(cmd: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed\n{result.stderr.strip()}")
    return result.stdout


def ensure_tools(*names: str) -> None:
    missing = [name for name in names if shutil.which(name) is None]
    if missing:
        raise SystemExit(f"Missing required tool(s): {', '.join(missing)}")


def clone_or_update(repo: dict[str, str]) -> None:
    WORK_REPOS.mkdir(parents=True, exist_ok=True)
    target = WORK_REPOS / repo["name"]
    if target.exists():
        run(["git", "pull", "--ff-only"], cwd=target)
        return
    run(["git", "clone", "--depth", "1", repo["url"], str(target)])


def first_existing(paths: list[Path]) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def read_intro(repo_dir: Path, max_chars: int = 4200) -> str:
    readme = first_existing(
        [
            repo_dir / "README.md",
            repo_dir / "readme.md",
            repo_dir / "README",
        ]
    )
    if not readme:
        return ""
    text = readme.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text[:max_chars].strip()


def repo_tree(repo_dir: Path, limit: int = 80) -> list[str]:
    paths: list[str] = []
    for path in sorted(repo_dir.rglob("*")):
        if ".git" in path.parts or path.is_dir():
            continue
        rel = path.relative_to(repo_dir).as_posix()
        if rel.startswith(("node_modules/", ".venv/", "data/")):
            continue
        paths.append(rel)
        if len(paths) >= limit:
            break
    return paths


def write_brief() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Selected GitHub Repositories",
        "",
        "These are the current repos selected for the personalized GitHub-to-podcast loop.",
        "",
    ]
    manifest = []
    for repo in DEFAULT_REPOS:
        clone_or_update(repo)
        repo_dir = WORK_REPOS / repo["name"]
        sha = run(["git", "rev-parse", "--short", "HEAD"], cwd=repo_dir).strip()
        remote = run(["git", "remote", "get-url", "origin"], cwd=repo_dir).strip()
        intro = read_intro(repo_dir, max_chars=1800)
        tree = repo_tree(repo_dir, limit=30)
        manifest.append({**repo, "commit": sha, "remote": remote})
        lines.extend(
            [
                f"## {repo['name']}",
                "",
                f"- Remote: {remote}",
                f"- Local commit: `{sha}`",
                f"- Role: {repo['role']}",
                "",
                "Top-level evidence:",
                "",
                "```text",
                "\n".join(tree),
                "```",
                "",
                "README excerpt:",
                "",
                "```text",
                intro,
                "```",
                "",
            ]
        )
    (OUTPUTS / "selected_repos.md").write_text("\n".join(lines), encoding="utf-8")
    (OUTPUTS / "selected_repos.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_dialogue(script_path: Path) -> list[DialogueTurn]:
    turns: list[DialogueTurn] = []
    current_speaker: str | None = None
    current_lines: list[str] = []

    speaker_re = re.compile(r"^\[(主持人|分析员|旁白)\]\s*$")
    for raw_line in script_path.read_text(encoding="utf-8").splitlines():
        match = speaker_re.match(raw_line.strip())
        if match:
            if current_speaker and current_lines:
                turns.append(DialogueTurn(current_speaker, "\n".join(current_lines).strip()))
            current_speaker = match.group(1)
            current_lines = []
            continue
        if current_speaker:
            line = raw_line.strip()
            if line and not line.startswith("#"):
                current_lines.append(line)
    if current_speaker and current_lines:
        turns.append(DialogueTurn(current_speaker, "\n".join(current_lines).strip()))
    return turns


def synthesize_audio(script_path: Path, output_path: Path, rate: int) -> None:
    ensure_tools("say", "ffmpeg")
    turns = parse_dialogue(script_path)
    if not turns:
        raise SystemExit(f"No dialogue turns found in {script_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="podcast_segments_") as tmp:
        tmp_path = Path(tmp)
        concat_file = tmp_path / "concat.txt"
        concat_lines = []
        for idx, turn in enumerate(turns, start=1):
            txt = tmp_path / f"{idx:03d}.txt"
            aiff = tmp_path / f"{idx:03d}.aiff"
            wav = tmp_path / f"{idx:03d}.wav"
            txt.write_text(turn.text, encoding="utf-8")
            voice = VOICE_MAP.get(turn.speaker, "Tingting")
            run(["say", "-v", voice, "-r", str(rate), "-f", str(txt), "-o", str(aiff)])
            run(
                [
                    "ffmpeg",
                    "-y",
                    "-v",
                    "error",
                    "-i",
                    str(aiff),
                    "-af",
                    "loudnorm=I=-18:TP=-2:LRA=11",
                    str(wav),
                ]
            )
            concat_lines.append(f"file '{wav.as_posix()}'")
        concat_file.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
        tmp_m4a = output_path.with_suffix(".tmp.m4a")
        run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c:a",
                "aac",
                "-b:a",
                "96k",
                "-movflags",
                "+faststart",
                str(tmp_m4a),
            ]
        )
        os.replace(tmp_m4a, output_path)


def duration_seconds(path: Path) -> float:
    ensure_tools("ffprobe")
    out = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ]
    )
    return float(out.strip())


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("brief")

    audio = sub.add_parser("audio")
    audio.add_argument("--script", type=Path, required=True)
    audio.add_argument("--output", type=Path, required=True)
    audio.add_argument("--rate", type=int, default=162)

    args = parser.parse_args()
    if args.command == "brief":
        ensure_tools("git")
        write_brief()
    elif args.command == "audio":
        synthesize_audio(args.script, args.output, args.rate)
        seconds = duration_seconds(args.output)
        print(f"Wrote {args.output} ({seconds / 60:.1f} min)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
