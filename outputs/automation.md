# Daily GitHub Research Automation

This is the operating contract for a recurring Codex or other Agent task. It is
a reference template; cloning the repository does not automatically create a
scheduled job.

## Schedule

- Check every 6 hours.
- Create at most one completed report per local calendar day.
- Run from the repository root.

## Start-of-run checks

1. Pull the latest `origin/main` with fast-forward only.
2. Inspect the current worktree before making changes.
3. Determine today's date in the project's local timezone.
4. Check `outputs/daily-research/` for today's completed report.
5. If the report exists, passes validation, and `main` is synchronized with the
   remote, exit without file changes or an empty commit.

## Research contract

When today's report is missing:

1. Select exactly one repository that has not already been covered.
2. Prefer practical relevance to raw popularity. Example domains include coding
   agents, Agent Skills and evaluation, workflow automation, AI media, knowledge
   management, browser/computer use, and AI productization.
3. Research from primary sources: the GitHub repository, README, documentation,
   releases, issues, and code where useful.
4. If cloning is needed, clone or update third-party repositories only under
   `work/repos/`. Never commit third-party source.
5. Write one substantial plain-Chinese report to
   `outputs/daily-research/YYYY-MM-DD_owner_repo.md`.
6. Record the repository link and exact revision inspected. Explain the problem,
   setup, architecture, reusable ideas, limitations, risks, practical fit, and a
   clear `use now`, `study only`, or `skip` recommendation.
7. Update `outputs/daily-research/index.md` without rewriting older reports unless
   correcting a factual error.

## Publication gate

Before publishing:

- Reject duplicates, generic summaries, fake findings, and timestamp-only edits.
- Run `skills/github-repo-research/scripts/validate_report.py`.
- Verify links, paths, tracked file sizes, and Git attribution.
- Scan intentional changes for credentials, third-party source, and private data.
- Stage only intentional files and use a descriptive commit message.
- Push only when the user or owning automation has explicit publishing authority.
- Verify that the remote commit matches local `HEAD`.

Never create mass external issues, unsolicited pull requests, empty commits, or
reports based only on search snippets.
