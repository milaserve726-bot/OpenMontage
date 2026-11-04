#!/usr/bin/env python3
"""Upload a rendered Mental Étudiant video and leave it private on YouTube.

Usage: python upload_youtube.py VIDEO.mp4 METADATA.json
METADATA.json must contain French ``title``, ``description`` and ``tags``.
OAuth credentials are read only from YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET,
and YOUTUBE_REFRESH_TOKEN in the environment (or the repository .env).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from tools.tool_registry import registry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path, help="Rendered MP4 to upload")
    parser.add_argument("metadata", type=Path, help="JSON file with title, description, and tags")
    args = parser.parse_args()

    try:
        metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
        title = str(metadata["title"]).strip()
        description = str(metadata["description"]).strip()
        tags = metadata["tags"]
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise ValueError("metadata.tags must be an array of strings")
        registry.discover()
        uploader = registry.get("youtube_auto_upload")
        if uploader is None:
            raise RuntimeError("youtube_auto_upload is not registered")
        result = uploader.execute({
            "video_path": str(args.video.resolve()),
            "title": title,
            "description": description,
            "tags": tags,
            "category_id": "27",  # YouTube category: Education
        })
        if not result.success:
            raise RuntimeError(result.error or "YouTube upload failed")
        print(json.dumps(result.data, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(f"YouTube upload failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
