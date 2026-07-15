# Daily GitHub Research Automation

Maintained in the Codex app:

- Name: Daily GitHub research
- Frequency: every 6 hours, creating at most one completed report per calendar day
- Workspace: `/Users/a1-6/Desktop/GitHub播客`
- Behavior:
  - Pull latest `origin/main` before work.
  - Exit without changes when today's verified report already exists.
  - Search for high-fit repositories around Codex/coding agents, Feishu/Lark automation, AI video, knowledge management, browser/computer-use automation, and AI FDE/productization.
  - Keep third-party repository clones under `work/repos/` only.
  - Write exactly one evidence-backed Chinese report under `outputs/daily-research/`.
  - Explain the problem, usage, architecture, reusable ideas, limitations, risks, and fit with the user's projects.
  - Maintain `outputs/daily-research/index.md`.
  - Record useful external fixes as review candidates; never send unsolicited PRs automatically.
  - Reject duplicates, generic summaries, fake findings, and timestamp-only changes.
  - Verify links, paths, secrets, oversized files, and Git author attribution.
  - Commit and push durable changes to `origin/main`.
  - Never commit API keys or cloned third-party source.
