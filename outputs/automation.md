# Automation

Created in Codex app:

- Name: Personal GitHub podcast radar
- Frequency: every 6 hours
- Workspace: `/Users/a1-6/Documents/Codex/2026-07-05/26-7-4-https-rn6vx-xetslk`
- Behavior:
  - Pull latest `origin/main` before work.
  - Search GitHub for high-fit repositories around Codex/coding agents, Feishu/Lark automation, knowledge management, RSS/news radar, repository ingestion, TTS/podcast generation, browser/computer-use automation, and AI FDE/productization.
  - Keep third-party repository clones under `work/repos/` only.
  - Update `outputs/selected_repos.*`.
  - Generate a new Chinese 10-40 minute podcast script and local-TTS `.m4a` only when there is materially new high-fit content.
  - Validate audio duration and decoding.
  - Commit and push durable changes to `origin/main`.
  - Avoid paid TTS/LLM APIs unless explicitly configured for this workflow.
