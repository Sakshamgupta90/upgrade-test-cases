"""Pick the projects CI should check: the case folders touched by this push or pull request.

Prints `python=[...]` and `node=[...]` (JSON lists of folder names) for $GITHUB_OUTPUT.
Runs every project on a manual run, or when the list of changed files can't be worked out.
"""

import json
import os
import subprocess
from pathlib import Path


def projects() -> dict[str, str]:
    found = {}
    for d in sorted(p for p in Path(".").iterdir() if p.is_dir() and not p.name.startswith(".")):
        if (d / "package.json").is_file():
            found[d.name] = "node"
        elif any((d / f).is_file() for f in ("requirements.txt", "pyproject.toml", "setup.py")):
            found[d.name] = "python"
    return found


def changed_folders() -> set[str] | None:
    event = os.environ.get("GITHUB_EVENT_NAME", "")
    if event == "pull_request":
        base = f"origin/{os.environ['GITHUB_BASE_REF']}"
    elif event == "push":
        base = os.environ.get("BEFORE_SHA", "")
        if not base or set(base) == {"0"}:  # first push of a branch: no "before"
            return None
    else:
        return None
    try:
        out = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD" if event == "pull_request" else f"{base}..HEAD"],
                             capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None
    return {line.split("/", 1)[0] for line in out.splitlines() if "/" in line}


all_projects = projects()
changed = changed_folders()
picked = {name: kind for name, kind in all_projects.items() if changed is None or name in changed}
lines = [f"{kind}={json.dumps([n for n, k in picked.items() if k == kind])}" for kind in ("python", "node")]
print("\n".join(lines))
with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as f:
    f.write("\n".join(lines) + "\n")
