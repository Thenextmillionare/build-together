# How we work

## Pick the right place

| Information | Home |
| --- | --- |
| Task, owner, acceptance criteria, status | Task issue |
| Session progress, findings, next action | Work log issue |
| Focused question or feedback request | Mentor review issue |
| Early project pitch | Project idea issue |
| Agreed scope and run instructions | Project folder README |
| Meeting agenda and decisions | Dated meeting note |
| Code review | Pull request |

## Task lifecycle

`status:next` → `status:doing` → `status:review` → close when done.

Move to `status:blocked` when stuck and state what would unblock you. Remove the old status label when adding another. The assignee is the person responsible for the next action; reassign when handing work over. Use `priority:high` sparingly.

A task is done when its acceptance criteria are met, evidence is linked, and the requested review has happened. Close abandoned tasks as not planned and explain why.

## A weekly 20-minute review

- 5 minutes: show a concrete result or useful learning.
- 5 minutes: inspect blockers and unanswered review requests.
- 5 minutes: discuss a design choice or experiment.
- 5 minutes: pick the next one to three tasks, with owners.

Copy the meeting template and link follow-ups to issues. Record decisions where future you can find them.

## Monitoring without busywork

The dashboard reads GitHub Issues, which remain the source of truth. A task is stale when it has had no issue activity for seven days. This is a conversation prompt, not a performance score. A comment resets that timer; it does not prove progress. Due dates are deliberately not inferred from prose. Use milestones if you want to agree on a delivery window.

Automation does not post reminders, send invitations, or close stale issues. Both people control the pace.
