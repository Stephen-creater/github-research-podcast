# Daily GitHub Research Podcast

Run every 6 hours and create at most one completed repository episode per day.

1. Pull `main` with fast-forward only and inspect the worktree.
2. If today's verified report, dialogue script, audio, and indexes already exist,
   exit without changes.
3. Build a private recent-project snapshot, then score candidates: direct project
   help 40%, reusable design 25%, maturity 15%, novelty 10%, momentum 10%.
4. Select one uncovered repository; raw stars cannot override weak project fit.
5. Research primary sources and pin the inspected commit.
6. In both report and dialogue, explain which recent project problem it helps,
   what to reuse, the smallest trial, and what should not be copied.
7. Generate MiMo TTS audio. The task is incomplete if audio is missing.
8. Validate the report, project-help segment, script markers, duration, and decode.
9. Update indexes, scan for secrets and oversized files, then commit and push only
   meaningful artifacts.

Keep third-party clones in `work/repos/`. Never commit credentials or cloned source,
create empty commits, or open unsolicited external issues and pull requests.
