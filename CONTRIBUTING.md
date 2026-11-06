# Contributing together

Anyone with repository write access can open issues, comment, create branches, and propose changes. Keep feedback specific, kind, and actionable.

## Small changes, clear reviews

1. Start from a task issue with a testable outcome.
2. Create a branch such as `feature/short-description` or `docs/meeting-notes`.
3. Make a focused change. Put project code under `projects/<project-name>/` with its own README and run instructions.
4. Open a pull request and link the task with `Closes #NUMBER` only when merging really completes the work.
5. Request the other person's review. Include what changed, how to try it, and evidence that it works.
6. Resolve feedback and merge when ready. For experiments, record what you learned even when you decide not to ship.

Requesting review is our working agreement; the repository does not enforce a branch protection rule by default. Use a normal issue comment for questions that do not need code changes.

## Work logs

Prefer one log per meaningful session. State what actually happened, link an artifact or commit when possible, and write the next step. Do not duplicate a log as a Markdown file unless it is a durable guide.

## Verification

For dashboard changes, run `python3 -m unittest discover -s tests -v`. For each new project, document its own meaningful checks. Keep credentials and private datasets out of commits.
