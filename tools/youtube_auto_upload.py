"""Scheduled YouTube uploads through the YouTube Data API v3.

OAuth refresh credentials are read from environment variables; secrets must
never be passed in tool inputs or written into project artifacts.
"""
from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path
import time
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)


YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
DEFAULT_CHANNEL_ID = "UCn0xh_GgYN-qdCkte6LUUDg"  # @mentaletudiant
TOKEN_URI = "https://oauth2.googleapis.com/token"


class YouTubeAutoUpload(BaseTool):
    name = "youtube_auto_upload"
    version = "1.0.0"
    tier = ToolTier.PUBLISH
    capability = "publish"
    provider = "youtube_data_api_v3"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    dependencies = [
        "python:google-api-python-client",
        "python:google-auth",
        "python:google-auth-httplib2",
        "python:google-auth-oauthlib",
    ]
    install_instructions = (
        "Install the Google YouTube Data API client dependencies and set "
        "YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, and YOUTUBE_REFRESH_TOKEN "
        "in .env. Enable YouTube Data API v3 in the "
        "Google Cloud project that issued the OAuth credentials."
    )
    capabilities = ["scheduled_video_upload", "custom_thumbnail_upload"]
    supports = {"scheduled_publish": True, "custom_thumbnail": True, "oauth_refresh_token": True}
    input_schema = {
        "type": "object",
        "required": ["video_path", "title", "description", "tags"],
        "properties": {
            "video_path": {"type": "string"},
            "title": {"type": "string", "minLength": 1, "maxLength": 100},
            "description": {"type": "string", "maxLength": 5000},
            "thumbnail_path": {"type": "string", "description": "Optional JPG/PNG thumbnail."},
            "tags": {"type": "array", "items": {"type": "string"}, "maxItems": 500},
            "publish_at": {"type": "string", "description": "Optional future RFC3339 timestamp; omit to leave the upload private."},
            "channel_id": {"type": "string", "default": DEFAULT_CHANNEL_ID},
            "category_id": {"type": "string", "default": "27"},
        },
    }
    output_schema = {
        "type": "object",
        "properties": {
            "video_id": {"type": "string"},
            "video_url": {"type": "string"},
            "channel_id": {"type": "string"},
            "publish_at": {"type": "string"},
            "thumbnail_set": {"type": "boolean"},
            "status": {"type": "string"},
        },
    }
    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=0, network_required=True)
    side_effects = ["uploads a video privately; optionally sets a thumbnail and schedules publication"]
    user_visible_verification = ["Verify returned channel ID, video URL, scheduled publication time, and thumbnail status"]

    def get_status(self) -> ToolStatus:
        if not all(os.getenv(k, "").strip() for k in (
            "YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"
        )):
            return ToolStatus.UNAVAILABLE
        try:
            import googleapiclient.discovery  # noqa: F401
            from google.oauth2.credentials import Credentials  # noqa: F401
            from google.auth.transport.requests import Request  # noqa: F401
        except ImportError:
            return ToolStatus.UNAVAILABLE
        return ToolStatus.AVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        return 0.0

    @staticmethod
    def _parse_publish_at(value: str) -> datetime:
        try:
            result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (TypeError, ValueError) as exc:
            raise ValueError("publish_at must be an RFC3339/ISO-8601 datetime with timezone") from exc
        if result.tzinfo is None:
            raise ValueError("publish_at must include a timezone offset")
        if result.timestamp() < time.time() + 20 * 60:
            raise ValueError("publish_at must be at least 20 minutes in the future")
        return result.astimezone(timezone.utc)

    @staticmethod
    def _youtube_client():
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        credentials = Credentials(
            token=None,
            refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"].strip(),
            token_uri=TOKEN_URI,
            client_id=os.environ["YOUTUBE_CLIENT_ID"].strip(),
            client_secret=os.environ["YOUTUBE_CLIENT_SECRET"].strip(),
            scopes=[YOUTUBE_UPLOAD_SCOPE, YOUTUBE_READONLY_SCOPE],
        )
        credentials.refresh(Request())
        return build("youtube", "v3", credentials=credentials, cache_discovery=False)

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        started = time.monotonic()
        try:
            if self.get_status() != ToolStatus.AVAILABLE:
                return ToolResult(
                    success=False,
                    error=("YouTube uploader is not configured. Install its Google API dependencies "
                           "and set YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, and YOUTUBE_REFRESH_TOKEN in the environment."),
                )

            video = Path(inputs["video_path"]).expanduser().resolve()
            thumbnail_value = inputs.get("thumbnail_path")
            thumbnail = Path(thumbnail_value).expanduser().resolve() if thumbnail_value else None
            if not video.is_file() or video.suffix.lower() not in {".mp4", ".mov", ".mkv", ".webm"}:
                raise ValueError(f"video_path must be an existing video file: {video}")
            if thumbnail is not None and (not thumbnail.is_file() or thumbnail.suffix.lower() not in {".jpg", ".jpeg", ".png"}):
                raise ValueError(f"thumbnail_path must be an existing JPG or PNG: {thumbnail}")

            title = str(inputs["title"]).strip()
            description = str(inputs["description"]).strip()
            tags = [str(tag).strip() for tag in inputs.get("tags", []) if str(tag).strip()]
            if not title or len(title) > 100:
                raise ValueError("YouTube title must contain 1–100 characters")
            if len(description) > 5000:
                raise ValueError("YouTube description must be at most 5000 characters")
            publish_at = self._parse_publish_at(inputs["publish_at"]) if inputs.get("publish_at") else None
            channel_id = str(inputs.get("channel_id") or DEFAULT_CHANNEL_ID).strip()

            youtube = self._youtube_client()
            channels = youtube.channels().list(part="id,snippet", mine=True).execute()
            owned_channels = channels.get("items", [])
            match = next((c for c in owned_channels if c.get("id") == channel_id), None)
            if match is None:
                found = ", ".join(c.get("id", "unknown") for c in owned_channels) or "none"
                raise PermissionError(
                    f"OAuth account does not own target channel {channel_id}; authorized channel IDs: {found}"
                )

            # Upload private first. Set the thumbnail before attaching publishAt,
            # so a thumbnail permission/error cannot accidentally publish a bare video.
            from googleapiclient.http import MediaFileUpload

            insert = youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description,
                        "tags": tags,
                        "categoryId": str(inputs.get("category_id", "27")),
                    },
                    "status": {"privacyStatus": "private"},
                },
                media_body=MediaFileUpload(str(video), mimetype="video/*", resumable=True, chunksize=8 * 1024 * 1024),
                notifySubscribers=True,
            )
            response = None
            while response is None:
                _, response = insert.next_chunk()
            video_id = response["id"]

            if thumbnail is not None:
                mime_type = "image/png" if thumbnail.suffix.lower() == ".png" else "image/jpeg"
                youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=MediaFileUpload(str(thumbnail), mimetype=mime_type, resumable=False),
                ).execute()

            if publish_at is not None:
                youtube.videos().update(
                    part="status",
                    body={
                        "id": video_id,
                        "status": {
                            "privacyStatus": "private",
                            "publishAt": publish_at.isoformat().replace("+00:00", "Z"),
                        },
                    },
                ).execute()

            return ToolResult(
                success=True,
                data={
                    "video_id": video_id,
                    "video_url": f"https://www.youtube.com/watch?v={video_id}",
                    "channel_id": channel_id,
                    "channel_title": match.get("snippet", {}).get("title"),
                    "publish_at": publish_at.isoformat().replace("+00:00", "Z") if publish_at else None,
                    "thumbnail_set": thumbnail is not None,
                    "status": "scheduled_private_until_publish_at" if publish_at else "private",
                },
                artifacts=[str(video)] + ([str(thumbnail)] if thumbnail is not None else []),
                duration_seconds=round(time.monotonic() - started, 2),
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=f"YouTube upload/scheduling failed: {type(exc).__name__}: {exc}",
                duration_seconds=round(time.monotonic() - started, 2),
            )
