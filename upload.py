#!/usr/bin/env python3
"""Publish the Mental Étudiant final horizontal video to its YouTube channel."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from lib.youtube_publish import EXPECTED_VIDEO_NAME, REPO_ROOT, publish_video


def _find_final() -> Path | None:
    matches = [path for path in REPO_ROOT.rglob(EXPECTED_VIDEO_NAME) if ".git" not in path.parts and ".venv" not in path.parts]
    return max(matches, key=lambda path: path.stat().st_mtime) if matches else None


def _project_root(video_path: Path) -> Path:
    projects_root = REPO_ROOT / "projects"
    for parent in video_path.parents:
        if parent.parent == projects_root:
            return parent
    return REPO_ROOT / "projects" / "mental-etudiant"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", nargs="?", type=Path, help=f"Defaults to the newest {EXPECTED_VIDEO_NAME} under projects/.")
    parser.add_argument("--metadata", type=Path, help="Optional French YouTube metadata JSON.")
    args = parser.parse_args()

    video = args.video.expanduser().resolve() if args.video else _find_final()
    if video is None or not video.is_file():
        print(f"Final video not found: {EXPECTED_VIDEO_NAME}", file=sys.stderr)
        return 2

    result = publish_video(video, _project_root(video), args.metadata)
    if not result.get("success"):
        print(result.get("error", "YouTube publishing failed."), file=sys.stderr)
        return 1
    print(f"LIAISON OK — {result.get('channel_title')} — {result.get('status')}")
    print(result.get("video_url", ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
