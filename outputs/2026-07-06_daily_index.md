# 2026-07-06 Daily Podcast Index

Daily target: at least 5 single-repository podcast episodes.

Status: done. All 5 episodes use one repository per episode, have script plus `.m4a` audio, are between 10 and 40 minutes, and passed `ffmpeg` decode verification.

| # | Repository | Fit role | Script | Audio | Duration | Status |
| --- | --- | --- | --- | --- | ---: | --- |
| 01 | `niuz3199-collab/Morning-news-podcast` | Android news-to-audio product reference for daily briefing, MiMo TTS, logging, and mobile listening. | `outputs/2026-07-06_morning_news_podcast_single_repo_script.md` | `outputs/2026-07-06_morning_news_podcast_single_repo.m4a` | 10.7 min | done |
| 02 | `yamadashy/repomix` | Repository-to-AI-context packer for deeper single-repo scripts and token/security gates. | `outputs/2026-07-06_repomix_single_repo_script.md` | `outputs/2026-07-06_repomix_single_repo.m4a` | 11.7 min | done |
| 03 | `browser-use/browser-use` | Browser execution layer for coding agents, GitHub evidence collection, and Feishu workflow automation. | `outputs/2026-07-06_browser_use_single_repo_script.md` | `outputs/2026-07-06_browser_use_single_repo.m4a` | 11.4 min | done |
| 04 | `microsoft/playwright-mcp` | MCP browser automation server for structured web interaction and complex page-state workflows. | `outputs/2026-07-06_playwright_mcp_single_repo_script.md` | `outputs/2026-07-06_playwright_mcp_single_repo.m4a` | 11.1 min | done |
| 05 | `DIYgod/RSSHub` | RSS route infrastructure reference for a durable personal repo/news radar input layer. | `outputs/2026-07-06_rsshub_single_repo_script.md` | `outputs/2026-07-06_rsshub_single_repo.m4a` | 11.8 min | done |

Verification:

- `python3 -m py_compile github_podcast_pipeline.py`
- `ffprobe` duration check for all 5 single-repo `.m4a` files:
  - `2026-07-06_morning_news_podcast_single_repo.m4a`: 642.56s
  - `2026-07-06_repomix_single_repo.m4a`: 704.48s
  - `2026-07-06_browser_use_single_repo.m4a`: 685.60s
  - `2026-07-06_playwright_mcp_single_repo.m4a`: 667.68s
  - `2026-07-06_rsshub_single_repo.m4a`: 707.04s
- `ffmpeg -v error -i <audio> -f null -` decode check for all 5 single-repo `.m4a` files

Operating note:

- Today's completed episodes intentionally avoid a final multi-repository roundup.
- Third-party repositories were cloned or updated only under `work/repos/`, which is ignored by git.
