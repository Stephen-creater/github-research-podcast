# Personal GitHub Research Lab

This workspace turns selected GitHub projects into durable Chinese research notes.
The earlier single-repository podcast episodes remain as an archive and can still
be generated on demand.

Important format rule: one repository equals one daily report. A discovery run may
inspect several candidates, but the maintained output studies exactly one repository.

Daily target: one evidence-backed repository report under `outputs/daily-research/`.
No empty commits or timestamp-only changes are allowed.

The optional audio path uses TokenDance's OpenAI-compatible MiMo TTS when
`TOKENDANCE_API_KEY` is provided through the environment or macOS Keychain.

## Current Pipeline

1. Select one repository that matches the user's active workflows and has not been covered.
2. Clone it into `work/repos/` when code inspection is needed.
3. Verify claims from the repository, documentation, releases, issues, and code.
4. Write a plain-Chinese report under `outputs/daily-research/`.
5. Maintain `outputs/daily-research/index.md`.
6. Check links, duplication, secrets, oversized files, and Git attribution.
7. Commit and push only meaningful durable artifacts to the private remote repository.

## Daily Research

See `outputs/daily-research/index.md`.

## Podcast Archive

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
