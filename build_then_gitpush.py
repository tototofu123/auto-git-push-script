#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run build command, then one-click git push"
    )
    parser.add_argument("--repo", default=".", help="Path to git repository")
    parser.add_argument(
        "--build-cmd",
        default="python -m pip --version",
        help="Build command to run before push",
    )
    parser.add_argument(
        "--message",
        default="",
        help="Commit message. If empty, prompt interactively.",
    )
    parser.add_argument("--branch", default="", help="Branch override")
    return parser.parse_args()


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def current_branch(repo: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def main() -> None:
    args = parse_args()
    repo = Path(args.repo).resolve()
    if not (repo / ".git").exists():
        raise SystemExit(f"Not a git repo: {repo}")

    print(f"Running build command: {args.build_cmd}")
    subprocess.run(args.build_cmd, cwd=repo, shell=True, check=True)

    message = args.message.strip() or input("Build finished. Commit message: ").strip()
    if not message:
        raise SystemExit("Commit message is required.")

    branch = args.branch.strip() or current_branch(repo)
    click = (
        input("Press Enter to auto git push now (or type n to cancel): ")
        .strip()
        .lower()
    )
    if click == "n":
        print("Cancelled.")
        return

    run(["git", "add", "-A"], repo)
    run(["git", "commit", "-m", message], repo)
    run(["git", "push", "-u", "origin", branch], repo)
    print("Auto git push complete.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(f"Command failed with code {exc.returncode}", file=sys.stderr)
        raise SystemExit(exc.returncode)
