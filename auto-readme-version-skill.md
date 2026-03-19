---
name: auto-readme-version
description: Automatically bump README semantic version and release notes on push/build events.
argument-hint: "<repo path or objective, optional>"
outputs:
  - README.md
  - docs/version-history.md
---

# Auto README Version Skill

Use this skill to keep repository README versioning up to date automatically.

## Versioning model

- `x.y.z` semantic versioning is required.
- `x` (`major`) = most important updates (breaking changes, architecture or security level changes).
- `y` (`minor`) = new features and significant non-breaking enhancements.
- `z` (`patch`) = minor updates (small fixes, docs tweaks, refactors, formatting).

## Trigger policy

Run this workflow on:

1. Every `git push`
2. Every build/release pipeline run
3. Manual release command execution

If no major/minor signal is found, default to patch bump (`z + 1`).

## Bump detection rules

Pick the highest matching level from commits included in the push/build window:

- `major` when commit messages include `BREAKING CHANGE`, `major:`, or a Conventional Commit with `!`
- `minor` when commit messages include `feat:` or `feature:`
- `patch` for all other change types (including docs/chore/fix/refactor)

## Required behavior

1. Ensure `README.md` has a version block (`Current Version: vX.Y.Z`).
2. Compute bump level from commit messages and change scope.
3. Increment version using semantic rules.
4. Update README with:
   - current version
   - bump type used
   - timestamp
5. Append a short entry to `docs/version-history.md`.
6. Create a commit: `chore(version): bump README to vX.Y.Z`.
7. Continue push/build flow using updated version metadata.

## Safety checks

- Never decrease version numbers.
- Never skip from `x.y.z` to invalid formats.
- Do not treat docs-only changes as major/minor unless explicitly marked.

## Output contract

Return a compact report containing:

- previous version
- new version
- bump reason
- updated files
