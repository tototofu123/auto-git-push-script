#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path


VERSION_RE = re.compile(r"Current Version:\s*v(\d+)\.(\d+)\.(\d+)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Auto bump README semantic version")
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument(
        "--event-json",
        default="",
        help="Path to GitHub event JSON payload (push event)",
    )
    return parser.parse_args()


def read_messages(event_json: str) -> list[str]:
    if not event_json:
        return []

    payload = json.loads(Path(event_json).read_text(encoding="utf-8"))
    commits = payload.get("commits", [])
    return [str(c.get("message", "")) for c in commits]


def bump_level(messages: list[str]) -> str:
    text = "\n".join(messages)
    if re.search(r"BREAKING CHANGE", text, flags=re.IGNORECASE):
        return "major"
    if re.search(r"(^|\n)\s*major:\s*", text, flags=re.IGNORECASE):
        return "major"
    if any(
        re.search(r"^[a-z]+(\([^)]+\))?!:", m.strip(), flags=re.IGNORECASE)
        for m in messages
    ):
        return "major"
    if re.search(r"(^|\n)\s*feat:\s*", text, flags=re.IGNORECASE):
        return "minor"
    if re.search(r"(^|\n)\s*feature:\s*", text, flags=re.IGNORECASE):
        return "minor"
    return "patch"


def parse_version(readme_text: str) -> tuple[int, int, int]:
    match = VERSION_RE.search(readme_text)
    if not match:
        return (0, 0, 0)
    return tuple(int(match.group(i)) for i in range(1, 4))


def bump_version(current: tuple[int, int, int], level: str) -> tuple[int, int, int]:
    major, minor, patch = current
    if level == "major":
        return (major + 1, 0, 0)
    if level == "minor":
        return (major, minor + 1, 0)
    return (major, minor, patch + 1)


def format_version(version: tuple[int, int, int]) -> str:
    return f"v{version[0]}.{version[1]}.{version[2]}"


def update_readme(readme_path: Path, new_v: str, level: str, timestamp: str) -> None:
    text = (
        readme_path.read_text(encoding="utf-8")
        if readme_path.exists()
        else "# Repository\n"
    )

    status_block = (
        "## Version Status\n\n"
        f"- Current Version: {new_v}\n"
        f"- Last Bump: {level}\n"
        f"- Last Updated: {timestamp}\n"
    )

    if "## Version Status" in text:
        text = re.sub(
            r"## Version Status\n(?:\n|.)*?(?=\n## |\Z)",
            status_block + "\n",
            text,
            count=1,
        )
    else:
        text = text.rstrip() + "\n\n" + status_block + "\n"

    readme_path.write_text(text, encoding="utf-8")


def append_history(
    history_path: Path, old_v: str, new_v: str, level: str, timestamp: str
) -> None:
    if not history_path.exists():
        history_path.parent.mkdir(parents=True, exist_ok=True)
        history_path.write_text("# Version History\n\n", encoding="utf-8")

    entry = f"## {new_v} - {timestamp}\n- Previous: {old_v}\n- Bump: {level}\n\n"
    with history_path.open("a", encoding="utf-8") as f:
        f.write(entry)


def main() -> None:
    args = parse_args()
    repo = Path(args.repo).resolve()
    readme_path = repo / "README.md"
    history_path = repo / "docs" / "version-history.md"

    readme_text = (
        readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    )
    current = parse_version(readme_text)
    messages = read_messages(args.event_json)
    level = bump_level(messages)
    next_version = bump_version(current, level)

    old_v = format_version(current)
    new_v = format_version(next_version)
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

    update_readme(readme_path, new_v, level, timestamp)
    append_history(history_path, old_v, new_v, level, timestamp)

    print(f"previous={old_v}")
    print(f"new={new_v}")
    print(f"bump={level}")


if __name__ == "__main__":
    main()
