---
name: auto-readme-version
description: Auto bump README semantic version and append release history during push/build.
argument-hint: "<repo path or objective, optional>"
uses:
  - auto-readme-version
outputs:
  - README.md
  - docs/version-history.md
---

# /auto-readme-version

$ARGUMENTS

---

Run local automation to keep README semantic version current.

Required behavior:

1. Detect commit range for current push/build.
2. Infer bump level using highest-priority match:
   - major: `BREAKING CHANGE`, `major:`, Conventional Commit `!`
   - minor: `feat:` or `feature:`
   - patch: default
3. Read current README version in `x.y.z` form.
4. Increment exactly one level and reset lower levels when needed.
5. Update README fields:
   - Current Version
   - Last Bump
   - Last Updated
6. Append release note to `docs/version-history.md`.
7. Commit with: `chore(version): bump README to vX.Y.Z`.

Return:

- previous version
- new version
- bump level
- updated files
