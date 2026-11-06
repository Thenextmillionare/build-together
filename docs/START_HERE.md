# Start here

## First five minutes

1. **Owner:** invite your mentor through repository **Settings → Collaborators → Add people**. They must accept before they can use this private repository.
2. Open **Actions → Set up workspace → Run workflow** once. This installs the labels used by the forms. It is safe to run again.
3. Open a **Project idea** issue together. Agree on one outcome that would make the first week worthwhile.
4. Break that outcome into one to three **Task** issues. Add an assignee and start with `status:next`.
5. After your first session, create a **Work log** and link the task.

## No terminal needed

Use **Issues → New issue** to choose a form. Comments support Markdown, checklists, links, and screenshots. To edit a document, open it, click the pencil, and propose the change on a new branch. Open a pull request so the other person can review it.

## Invite your mentor

Suggested invitation text to copy yourself:

> I've set up Build Together as our shared workspace. We can track small tasks, log experiments, comment on progress, and review code here. Once you accept the GitHub invitation, start with the README and our first project idea.

## What the dashboard does

[DASHBOARD.md](../DASHBOARD.md) shows active tasks, blockers, requests for input, recent logs, and tasks without an update for seven days. Comments count as activity. Pull requests are reviewed in the **Pull requests** tab and do not count as tasks.

It refreshes on issue changes, comments, a daily schedule, or **Actions → Refresh dashboard → Run workflow**. The timestamp shows its last successful snapshot. If Actions are disabled or repository policy blocks automated commits, the issue links in the README still work; check the failed run in Actions.

## Optional local setup

Requires Git, GitHub CLI, and Python 3.11 or newer. No Python packages are needed.

```sh
gh repo clone Thenextmillionare/build-together
cd build-together
python3 -m unittest discover -s tests -v
```
