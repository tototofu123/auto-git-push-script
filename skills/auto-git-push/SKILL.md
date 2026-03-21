---
name: auto-git-push
description: Generate git add/commit/push command and optionally execute one-click push.
argument-hint: "<repo path and commit message, optional>"
---

# Auto Git Push

When the user is done coding and asks to push to GitHub:

1. Resolve repo path (default `.`) and current branch.
2. Resolve commit message.
3. Generate this command for copy/paste:
   - `git add -A && git commit -m "..." && git push -u origin <branch>`
4. If one-click push is requested, run:
   - `python auto_git_push.py --repo <path> --message "..." --auto`

Use `python auto_git_push.py --repo . --gui` for a click-based UI.
