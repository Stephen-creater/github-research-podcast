# Personal GitHub Podcast Lab

This workspace turns selected GitHub projects into a personalized Chinese audio briefing.

The first version deliberately uses zero-added-cost local macOS TTS, so the whole loop can run without ElevenLabs, OpenAI TTS, or another paid voice API. The tradeoff is voice quality: it is good enough to validate the workflow, not final broadcast quality.

## Current Pipeline

1. Select GitHub repositories that match the user's active workflows.
2. Clone them into `work/repos/` for local inspection.
3. Summarize the useful parts into `outputs/`.
4. Write a Chinese podcast script.
5. Convert the script into an `.m4a` audio file with macOS `say` and `ffmpeg`.
6. Commit and push durable artifacts to the private remote repository.

## Selected Repos

See `outputs/selected_repos.md`.

## Run Locally

Generate or refresh repo notes:

```bash
python3 github_podcast_pipeline.py brief
```

Generate audio from a dialogue script:

```bash
python3 github_podcast_pipeline.py audio \
  --script outputs/2026-07-05_github_personal_podcast_script.md \
  --output outputs/2026-07-05_github_personal_podcast.m4a
```

The script only uses Python standard library, macOS `say`, and `ffmpeg`.

## Storage Rule

User-facing scripts, notes, manifests, and audio outputs are committed and pushed. Cloned third-party repositories and temporary synthesis chunks are ignored.
