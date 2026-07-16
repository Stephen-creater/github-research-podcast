#!/usr/bin/env python3
"""Legacy helpers for repository briefs and optional Chinese podcast audio.

The maintained daily-research workflow now lives in the github-repo-research
Skill. This module preserves the original deterministic brief and audio tools.
"""

from __future__ import annotations

import argparse
import base64
import getpass
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
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


MIMO_VOICE_MAP = {
    "主持人": "白桦",
    "分析员": "茉莉",
    "旁白": "白桦",
}

MIMO_STYLE_MAP = {
    "主持人": "中文播客男主持，声音自然、有真人感，语速中等，像在认真解释一个技术项目。不要机械播报，不要夸张表演。",
    "分析员": "中文播客女分析员，声音自然、清晰、克制，有思考感，像在做项目复盘。不要机械播报，不要广告腔。",
    "旁白": "中文播客旁白，声音自然、平稳、可信，语速中等偏慢。",
}

TOKENDANCE_CHAT_COMPLETIONS_URL = "https://tokendance.space/gateway/v1/chat/completions"


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


def tokendance_key(prompt_key: bool) -> str:
    key = os.environ.get("TOKENDANCE_API_KEY", "").strip()
    if key:
        return key
    keychain_key = read_tokendance_key_from_keychain()
    if keychain_key:
        return keychain_key
    if prompt_key:
        return getpass.getpass("TokenDance key: ").strip()
    raise SystemExit("Set TOKENDANCE_API_KEY, store it in macOS Keychain, or pass --prompt-key.")


def read_tokendance_key_from_keychain() -> str | None:
    """Read TokenDance API key from macOS Keychain when available."""
    if sys.platform != "darwin" or shutil.which("security") is None:
        return None
    try:
        result = subprocess.run(
            [
                "security",
                "find-generic-password",
                "-a",
                "github-podcast",
                "-s",
                "tokendance-api-key",
                "-w",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def call_mimo_tts(text: str, speaker: str, key: str, model: str, voice: str | None = None) -> bytes:
    selected_voice = voice or MIMO_VOICE_MAP.get(speaker, "白桦")
    style = MIMO_STYLE_MAP.get(speaker, MIMO_STYLE_MAP["旁白"])
    body = {
        "model": model,
        "messages": [
            {"role": "user", "content": style},
            {"role": "assistant", "content": text},
        ],
        "audio": {
            "format": "wav",
            "voice": selected_voice,
        },
    }
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        TOKENDANCE_CHAT_COMPLETIONS_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    last_error = ""
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                raw = response.read()
            data = json.loads(raw)
            audio = data["choices"][0]["message"].get("audio") or {}
            audio_data = audio.get("data")
            if not audio_data:
                raise RuntimeError(f"No audio data in response: {json.dumps(data, ensure_ascii=False)[:500]}")
            return base64.b64decode(audio_data)
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")[:500]
            last_error = f"HTTP {error.code}: {detail}"
        except Exception as error:  # noqa: BLE001 - surface provider failures with context
            last_error = f"{type(error).__name__}: {error}"
        if attempt < 3:
            time.sleep(2 * attempt)
    raise RuntimeError(f"MiMo TTS failed for {speaker}: {last_error}")


def synthesize_mimo_audio(
    script_path: Path,
    output_path: Path,
    key: str,
    model: str,
    host_voice: str | None,
    analyst_voice: str | None,
) -> None:
    ensure_tools("ffmpeg")
    turns = parse_dialogue(script_path)
    if not turns:
        raise SystemExit(f"No dialogue turns found in {script_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="mimo_podcast_segments_") as tmp:
        tmp_path = Path(tmp)
        concat_file = tmp_path / "concat.txt"
        concat_lines = []
        for idx, turn in enumerate(turns, start=1):
            voice = None
            if turn.speaker == "主持人":
                voice = host_voice
            elif turn.speaker == "分析员":
                voice = analyst_voice
            wav = tmp_path / f"{idx:03d}_{turn.speaker}.wav"
            normalized = tmp_path / f"{idx:03d}_{turn.speaker}_norm.wav"
            print(f"Synthesizing {idx}/{len(turns)} {turn.speaker}", flush=True)
            wav.write_bytes(call_mimo_tts(turn.text, turn.speaker, key, model, voice=voice))
            run(
                [
                    "ffmpeg",
                    "-y",
                    "-v",
                    "error",
                    "-i",
                    str(wav),
                    "-af",
                    "loudnorm=I=-18:TP=-2:LRA=11",
                    str(normalized),
                ]
            )
            concat_lines.append(f"file '{normalized.as_posix()}'")
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
                "128k",
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

    mimo = sub.add_parser("audio-mimo")
    mimo.add_argument("--script", type=Path, required=True)
    mimo.add_argument("--output", type=Path, required=True)
    mimo.add_argument("--model", default="mimo-v2.5-tts")
    mimo.add_argument("--host-voice", default="白桦")
    mimo.add_argument("--analyst-voice", default="茉莉")
    mimo.add_argument("--prompt-key", action="store_true")

    args = parser.parse_args()
    if args.command == "brief":
        ensure_tools("git")
        write_brief()
    elif args.command == "audio":
        synthesize_audio(args.script, args.output, args.rate)
        seconds = duration_seconds(args.output)
        print(f"Wrote {args.output} ({seconds / 60:.1f} min)")
    elif args.command == "audio-mimo":
        key = tokendance_key(args.prompt_key)
        synthesize_mimo_audio(
            args.script,
            args.output,
            key,
            args.model,
            args.host_voice,
            args.analyst_voice,
        )
        seconds = duration_seconds(args.output)
        print(f"Wrote {args.output} ({seconds / 60:.1f} min)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
