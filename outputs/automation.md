# Automation

Created in Codex app:

- Name: Personal GitHub podcast radar
- Frequency: every 6 hours
- Workspace: `/Users/a1-6/Desktop/GitHub播客`
- Behavior:
  - Pull latest `origin/main` before work.
  - Search GitHub for high-fit repositories around Codex/coding agents, Feishu/Lark automation, knowledge management, RSS/news radar, repository ingestion, TTS/podcast generation, browser/computer-use automation, and AI FDE/productization.
  - Keep third-party repository clones under `work/repos/` only.
  - Update `outputs/selected_repos.*`.
  - Pick exactly one repository per episode. Do not make a multi-repository roundup episode.
  - Generate a new Chinese 10-40 minute podcast script and MiMo TTS `.m4a` focused on that one repository only when there is materially new high-fit content and `TOKENDANCE_API_KEY` is available.
  - Each episode should directly explain the repository: problem, usage, code architecture, key design choices, limitations, and concrete fit with the user's projects.
  - Validate audio duration and decoding.
  - Commit and push durable changes to `origin/main`.
  - Avoid paid TTS/LLM APIs unless explicitly configured for this workflow. Never commit API keys.
