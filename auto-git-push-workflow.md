---
name: auto-git-push
description: Build the git push command and optionally execute it after user confirmation or one-click action.
argument-hint: "<repo path and commit message, optional>"
uses:
  - auto-git-push
outputs:
  - generated command
  - push status
---

# /auto-git-push

$ARGUMENTS

---

Workflow:

1. Validate repository path.
2. Resolve active branch.
3. Resolve commit message.
4. Print copy/paste command for terminal.
5. If one-click mode requested, execute auto push flow.
6. Return concise report with:
   - repository
   - branch
   - command
   - execution result
