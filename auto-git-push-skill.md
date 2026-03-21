---
name: auto-git-push
description: Generate safe git push commands and optionally run one-click auto push for the active repository.
argument-hint: "<repo path, optional>"
outputs:
  - terminal command string
  - optional git push execution
---

# Auto Git Push Skill

Use this skill when a user says they are done coding and want to publish to GitHub quickly.

## Behavior

1. Detect repository path and current branch.
2. Ask for commit message if not provided.
3. Generate a copy/paste command:
   - `git add -A && git commit -m "..." && git push -u origin <branch>`
4. Offer clipboard copy.
5. If user requests one-click push, run:
   - `python auto_git_push.py --repo <path> --message "..." --auto`

## Safety

- Stop if target is not a git repository.
- Do not run destructive git commands.
- Keep default push target as `origin <current-branch>` unless explicitly overridden.

## Quick commands

- Generate + copy flow: `python auto_git_push.py --repo .`
- Generate + auto copy: `python auto_git_push.py --repo . --copy`
- One-click auto push: `python auto_git_push.py --repo . --message "chore: update" --auto`
- GUI mode: `python auto_git_push.py --repo . --gui`
