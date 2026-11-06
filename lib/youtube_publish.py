"""Publish the Mental Étudiant final video to its verified YouTube channel."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
EXPECTED_CHANNEL_ID = "UCn0xh_GgYN-qdCkte6LUUDg"
EXPECTED_VIDEO_NAME = "FINAL_8MIN_100TOOLS_HENRI_HORIZONTAL.mp4"
DEFAULT_PROJECT = REPO_ROOT / "projects" / "mental-etudiant"


def _metadata(project_dir: Path, metadata_path: str | Path | None) -> dict[str, Any]:
    candidates = [Path(metadata_path)] if metadata_path else [
        project_dir / "artifacts" / "youtube_package.json",
        project_dir / "artifacts" / "youtube_metadata.json",
    ]
    for candidate in candidates:
        path = candidate if candidate.is_absolute() else REPO_ROOT / candidate
        if not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        candidates = data.get("title_options") or data.get("title_candidates") or []
        title = _strongest_title(candidates, data.get("selected_title") or data.get("title"))
        description = str(data.get("description") or "").strip()
        tags = data.get("tags", data.get("hashtags", []))
        thumbnail = data.get("thumbnail_path") or data.get("thumbnail")
        if not title or not description or not thumbnail:
            continue
        if not isinstance(tags, list):
            tags = []
        thumbnail_path = Path(str(thumbnail))
        if not thumbnail_path.is_absolute():
            thumbnail_path = REPO_ROOT / thumbnail_path
        return {
            "title": title[:100],
            "description": description[:5000],
            "tags": [str(tag).strip() for tag in tags if str(tag).strip()],
            "thumbnail_path": thumbnail_path,
        }
    raise FileNotFoundError("French YouTube metadata and thumbnail were not found")


def _strongest_title(candidates: Any, selected: Any) -> str:
    options = [str(value).strip() for value in candidates if str(value).strip()] if isinstance(candidates, list) else []
    fallback = str(selected or "").strip()
    if fallback and fallback not in options:
        options.append(fallback)
    if not options:
        return ""
    strong_phrases = ("change ta vie", "deviens", "arrête", "le secret", "personne ne te dit", "tu n'arrives", "tu n’arrives")
    direct_address = (" tu ", " ton ", " ta ", " tes ")
    benefits = ("concentration", "mémoire", "examens", "partiels", "bac", "réussir", "réussite", "réviser")
    def score(title: str) -> tuple[int, int]:
        text = f" {title.casefold()} "
        points = 4 * sum(phrase in text for phrase in strong_phrases)
        points += 2 * sum(word in text for word in direct_address)
        points += 2 * sum(word in text for word in benefits)
        points += 2 if "?" in title or "!" in title else 0
        return points, -len(title)
    return max(options, key=score)[:100]


def _youtube_thumbnail(source: Path, destination: Path) -> None:
    from PIL import Image, ImageOps

    if not source.is_file():
        raise FileNotFoundError("YouTube thumbnail file was not found")
    with Image.open(source) as image:
        fitted = ImageOps.fit(image.convert("RGB"), (1280, 720), method=Image.Resampling.LANCZOS)
        fitted.save(destination, format="JPEG", quality=92, optimize=True)


def publish_video(
    video_path: str | Path,
    project_dir: str | Path = DEFAULT_PROJECT,
    metadata_path: str | Path | None = None,
) -> dict[str, Any]:
    """Upload the named final MP4 publicly, with matching metadata and thumbnail."""
    path = Path(video_path).expanduser().resolve()
    project = Path(project_dir).expanduser().resolve()
    try:
        if path.name != EXPECTED_VIDEO_NAME:
            return {"success": False, "error": f"Only {EXPECTED_VIDEO_NAME} can be published by this action."}
        if not path.is_file():
            return {"success": False, "error": "Final Mental Étudiant MP4 was not found."}
        package = _metadata(project, metadata_path)

        # ToolRegistry loads the existing project .env without exposing values.
        from tools.tool_registry import registry

        registry.discover()
        uploader = registry.get("youtube_auto_upload")
        if uploader is None:
            return {"success": False, "error": "YouTube uploader is unavailable."}

        with tempfile.TemporaryDirectory(prefix="mental-etudiant-youtube-") as tmp:
            thumbnail = Path(tmp) / "thumbnail-1280x720.jpg"
            _youtube_thumbnail(package["thumbnail_path"], thumbnail)
            result = uploader.execute({
                "video_path": str(path),
                "title": package["title"],
                "description": package["description"],
                "tags": package["tags"],
                "thumbnail_path": str(thumbnail),
                "channel_id": EXPECTED_CHANNEL_ID,
                "category_id": "27",
            })
        if not result.success:
            return {"success": False, "error": result.error or "YouTube upload failed."}
        data = result.data or {}
        return {
            "success": True,
            "video_url": data.get("video_url"),
            "channel_title": data.get("channel_title"),
            "status": data.get("status"),
            "thumbnail_set": data.get("thumbnail_set", False),
            "title": package["title"],
        }
    except Exception as exc:
        # Do not relay exception text from OAuth/network libraries to the UI.
        return {"success": False, "error": f"YouTube publishing failed: {type(exc).__name__}."}
