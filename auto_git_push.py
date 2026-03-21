#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate copy-paste git push commands for a repository"
    )
    parser.add_argument("--repo", default=".", help="Path to the git repository")
    parser.add_argument(
        "--message",
        default="",
        help="Commit message. If empty, script prompts for it.",
    )
    parser.add_argument(
        "--branch",
        default="",
        help="Branch name override. Defaults to current branch.",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy generated command to clipboard on Windows.",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run git add/commit/push immediately.",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Open click-to-push desktop UI.",
    )
    return parser.parse_args()


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def current_branch(repo: Path) -> str:
    return run_git(repo, "rev-parse", "--abbrev-ref", "HEAD")


def copy_to_clipboard(text: str) -> bool:
    try:
        subprocess.run(["clip"], input=text, text=True, check=True)
        return True
    except Exception:
        return False


def escape_message(message: str) -> str:
    return message.replace('"', '\\"')


def build_command(message: str, branch: str) -> str:
    safe_message = escape_message(message)
    return (
        f'git add -A && git commit -m "{safe_message}" && git push -u origin {branch}'
    )


def run_auto_push(repo: Path, message: str, branch: str) -> None:
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", message], cwd=repo, check=True)
    subprocess.run(["git", "push", "-u", "origin", branch], cwd=repo, check=True)


def run_gui(repo: Path, branch: str) -> None:
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.title("Auto Git Push")
    root.geometry("720x280")

    tk.Label(root, text=f"Repo: {repo}", anchor="w").pack(
        fill="x", padx=12, pady=(12, 4)
    )
    tk.Label(root, text=f"Branch: {branch}", anchor="w").pack(
        fill="x", padx=12, pady=(0, 8)
    )
    tk.Label(root, text="Commit message", anchor="w").pack(fill="x", padx=12)

    message_var = tk.StringVar()
    entry = tk.Entry(root, textvariable=message_var)
    entry.pack(fill="x", padx=12, pady=(4, 8))
    entry.focus_set()

    output = tk.Text(root, height=6, wrap="word")
    output.pack(fill="both", expand=True, padx=12, pady=(0, 10))

    def show_command() -> None:
        message = message_var.get().strip()
        if not message:
            messagebox.showerror("Missing message", "Commit message is required.")
            return
        cmd = build_command(message, branch)
        output.delete("1.0", tk.END)
        output.insert("1.0", cmd)

    def copy_cmd() -> None:
        cmd = output.get("1.0", tk.END).strip()
        if not cmd:
            show_command()
            cmd = output.get("1.0", tk.END).strip()
        if not cmd:
            return
        root.clipboard_clear()
        root.clipboard_append(cmd)
        messagebox.showinfo("Copied", "Command copied to clipboard.")

    def auto_push_now() -> None:
        message = message_var.get().strip()
        if not message:
            messagebox.showerror("Missing message", "Commit message is required.")
            return
        try:
            run_auto_push(repo, message, branch)
            messagebox.showinfo("Done", "Git push completed.")
        except subprocess.CalledProcessError as exc:
            messagebox.showerror(
                "Git failed", f"Command failed with code {exc.returncode}."
            )

    row = tk.Frame(root)
    row.pack(fill="x", padx=12, pady=(0, 12))
    tk.Button(row, text="Generate Command", command=show_command).pack(side="left")
    tk.Button(row, text="Copy Command", command=copy_cmd).pack(side="left", padx=(8, 0))
    tk.Button(row, text="Auto Push Now", command=auto_push_now).pack(
        side="left", padx=(8, 0)
    )

    root.mainloop()


def main() -> None:
    args = parse_args()
    repo = Path(args.repo).resolve()

    if not (repo / ".git").exists():
        raise SystemExit(f"Not a git repo: {repo}")

    branch = args.branch.strip() or current_branch(repo)

    if args.gui:
        run_gui(repo, branch)
        return

    message = args.message.strip() or input("Commit message: ").strip()
    if not message:
        raise SystemExit("Commit message is required.")

    if args.auto:
        run_auto_push(repo, message, branch)
        print("Git push completed.")
        return

    command = build_command(message, branch)

    print("\nCopy and paste this command in CMD/PowerShell:\n")
    print(command)

    should_copy = args.copy
    if not should_copy:
        reply = input("\nCopy command to clipboard now? [Y/n]: ").strip().lower()
        should_copy = reply in ("", "y", "yes")

    if should_copy:
        if copy_to_clipboard(command):
            print("\nCopied to clipboard.")
        else:
            print("\nClipboard copy failed. You can still copy from terminal output.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(f"Git command failed with code {exc.returncode}.", file=sys.stderr)
        raise SystemExit(exc.returncode)
