# auto-gitpush-version-update

Auto bump `README.md` version on every `git push` (and manual run) using semantic versioning.

## What it does

- Maintains `x.y.z` version in `README.md` under a `Version Status` block.
- Chooses bump level from pushed commit messages:
  - `major`: `BREAKING CHANGE`, `major:`, or Conventional Commit `!`
  - `minor`: `feat:` or `feature:`
  - `patch`: default fallback
- Updates:
  - `README.md` (Current Version, Last Bump, Last Updated)
  - `docs/version-history.md` (append release entry)
- Commits and pushes the version update automatically via GitHub Actions.

## Files

- `auto-readme-version-skill.md`
- `auto-readme-version-workflow.md`
- `scripts/auto_readme_version.py`
- `.github/workflows/auto-readme-version.yml`

## Trigger behavior

- Runs on push.
- Runs manually with workflow dispatch.
- Prevents infinite loops by skipping runs from `github-actions[bot]` and ignoring push events where only `README.md` and `docs/version-history.md` changed.

## Version rules

- `x` (major): breaking/high-impact changes.
- `y` (minor): new non-breaking features.
- `z` (patch): fixes/docs/chore/minor updates.

## Manual local run

```bash
python scripts/auto_readme_version.py --repo .
```

## Optional install targets

If you want to reuse this as a portable skill/workflow package:

- OpenCode skill: `~/.config/opencode/skills/auto-readme-version/SKILL.md`
- Claude skill: `~/.claude/skills/auto-readme-version/SKILL.md`
- Codex skill: `~/.codex/skills/auto-readme-version/SKILL.md`
- Antigravity workflow: `~/.gemini/antigravity/global_workflows/auto-readme-version.md`
- Gemini command: `~/.gemini/commands/auto-readme-version.md`

## Version Status

- Current Version: v0.0.1
- Last Bump: patch
- Last Updated: 2026-03-19 15:45:56Z

