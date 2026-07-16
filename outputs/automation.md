# Daily GitHub Research Podcast

Run every 6 hours and create at most one completed repository episode per day.

1. Pull `main` with fast-forward only and inspect the worktree.
2. If today's verified report, dialogue script, audio, and indexes already exist,
   exit without changes.
3. Select one uncovered repository based on user fit, not raw popularity.
4. Research primary sources and pin the inspected commit.
5. Write the Chinese report, then derive a `[主持人]` / `[分析员]` script from it.
6. Generate MiMo TTS audio. The task is incomplete if audio is missing.
7. Validate the report, script markers, audio duration, and full decode.
8. Update indexes, scan for secrets and oversized files, then commit and push only
   meaningful artifacts.

Keep third-party clones in `work/repos/`. Never commit credentials or cloned source,
create empty commits, or open unsolicited external issues and pull requests.
