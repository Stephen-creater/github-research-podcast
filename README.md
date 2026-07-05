# Personal GitHub Podcast Lab

This workspace turns selected GitHub projects into personalized Chinese audio briefings.

Important format rule: one repository equals one episode. A discovery run may inspect many repositories, but the actual podcast script and audio must focus on exactly one repository.

The current audio path uses TokenDance's OpenAI-compatible MiMo TTS when `TOKENDANCE_API_KEY` is provided. The older zero-cost macOS `say` path remains only as a fallback for workflow testing; its voice quality is not acceptable as a user-facing podcast.

## Current Pipeline

1. Select GitHub repositories that match the user's active workflows.
2. Clone them into `work/repos/` for local inspection.
3. Pick one repository for the episode.
4. Summarize that repository's useful parts into `outputs/`.
5. Write a Chinese podcast script focused on that one repository.
6. Convert the script into an `.m4a` audio file with TokenDance MiMo TTS and `ffmpeg`.
7. Commit and push durable artifacts to the private remote repository.

## Selected Repos

See `outputs/selected_repos.md`.

## Run Locally

Generate or refresh repo notes:

```bash
python3 github_podcast_pipeline.py brief
```

Generate production audio from a single-repository dialogue script:

```bash
export TOKENDANCE_API_KEY=...
python3 github_podcast_pipeline.py audio-mimo \
  --script outputs/2026-07-05_gitingest_single_repo_script.md \
  --output outputs/2026-07-05_gitingest_single_repo.m4a
```

For a throwaway local workflow test only:

```bash
python3 github_podcast_pipeline.py audio \
  --script outputs/2026-07-05_github_personal_podcast_script.md \
  --output work/local_say_test.m4a
```

Do not use the local `say` output as a final listening artifact.

## Storage Rule

User-facing scripts, notes, manifests, and audio outputs are committed and pushed. Cloned third-party repositories, temporary synthesis chunks, and API keys are ignored.
