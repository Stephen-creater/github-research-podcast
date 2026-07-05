# Automation

Created in Codex app:

- Name: Personal GitHub podcast radar
- Frequency: daily
- Workspace: `/Users/a1-6/Desktop/GitHub播客`
- Behavior:
  - Pull latest `origin/main` before work.
  - Search GitHub for high-fit repositories around Codex/coding agents, Feishu/Lark automation, knowledge management, RSS/news radar, repository ingestion, TTS/podcast generation, browser/computer-use automation, and AI FDE/productization.
  - Keep third-party repository clones under `work/repos/` only.
  - Update `outputs/selected_repos.*`.
  - Generate at least 5 completed podcast episodes per calendar day.
  - Pick exactly one repository per episode. Do not make a multi-repository roundup episode as a final output.
  - Generate Chinese 10-40 minute podcast scripts and MiMo TTS `.m4a` files focused on one repository each when `TOKENDANCE_API_KEY` is available through the environment or macOS Keychain.
  - Each episode should directly explain the repository: problem, usage, code architecture, key design choices, limitations, and concrete fit with the user's projects.
  - Maintain a daily index under `outputs/` with repo, script, audio, duration, and status for every episode.
  - Validate audio duration and decoding.
  - If a script exists but audio failed, retry audio only. If audio is valid, do not regenerate it unless explicitly requested.
  - Commit and push durable changes to `origin/main`.
  - Avoid paid TTS/LLM APIs unless explicitly configured for this workflow. Never commit API keys.
