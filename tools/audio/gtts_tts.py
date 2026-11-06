"""French gTTS narration with optional calm-style post-processing."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)


class GTTSTTS(BaseTool):
    name = "gtts_tts"
    version = "0.1.0"
    tier = ToolTier.VOICE
    capability = "tts"
    provider = "gtts"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.HYBRID

    dependencies = ["python:gTTS", "python:imageio-ffmpeg", "network:gTTS"]
    install_instructions = "Install gTTS and imageio-ffmpeg in the active Python environment. gTTS requires outbound network access."
    agent_skills = ["text-to-speech"]
    capabilities = ["text_to_speech", "language_selection", "speed_postprocessing", "offline_postprocessing"]
    supports = {"voice_cloning": False, "multilingual": True, "offline": False, "native_audio": True}
    best_for = ["basic multilingual narration when no TTS credentials are available", "French narration with locally applied pacing and pauses"]
    not_good_for = ["named voice identity or voice cloning", "emotion and timbre control at the provider"]
    input_schema = {
        "type": "object",
        "required": ["text", "output_path"],
        "properties": {
            "text": {"type": "string", "minLength": 1},
            "lang": {"type": "string", "default": "fr"},
            "slow": {"type": "boolean", "default": False},
            "voice_style": {"type": "string", "default": "calm"},
            "rate": {"type": "number", "minimum": 0.5, "maximum": 2.0, "default": 0.85},
            "pitch_scale": {"type": "number", "minimum": 0.8, "maximum": 1.2, "default": 0.97},
            "pause_seconds": {"type": "number", "minimum": 0.0, "maximum": 2.0, "default": 0.45},
            "target_duration_seconds": {"type": "number", "minimum": 1.0, "maximum": 600.0},
            "output_path": {"type": "string"},
        },
    }
    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=256, disk_mb=100, network_required=True)
    retry_policy = RetryPolicy(max_retries=1, retryable_errors=["timeout", "connection"])
    idempotency_key_fields = ["text", "lang", "slow", "rate", "pitch_scale", "pause_seconds", "target_duration_seconds"]
    side_effects = ["sends narration text to Google Translate TTS", "writes MP3 to output_path"]
    user_visible_verification = ["Listen for intelligibility, pacing, and pause placement"]

    def get_status(self) -> ToolStatus:
        try:
            import gtts  # noqa: F401
            import imageio_ffmpeg

            return ToolStatus.AVAILABLE if Path(imageio_ffmpeg.get_ffmpeg_exe()).is_file() else ToolStatus.UNAVAILABLE
        except Exception:
            return ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        # gTTS is an unofficial Google Translate endpoint; no per-request price is exposed.
        return 0.0

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        if self.get_status() != ToolStatus.AVAILABLE:
            return ToolResult(success=False, error="gTTS or the bundled FFmpeg binary is unavailable; install gTTS and imageio-ffmpeg.")
        started = time.monotonic()
        try:
            result = self._generate(inputs)
            result.duration_seconds = round(time.monotonic() - started, 2)
            return result
        except Exception as exc:
            return ToolResult(success=False, error=f"gTTS narration failed: {exc}", duration_seconds=round(time.monotonic() - started, 2))

    def _generate(self, inputs: dict[str, Any]) -> ToolResult:
        from gtts import gTTS
        import imageio_ffmpeg

        text = str(inputs["text"]).strip()
        output_path = Path(inputs["output_path"])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        rate = float(inputs.get("rate", 0.85))
        pitch_scale = float(inputs.get("pitch_scale", 0.97))
        pause_seconds = float(inputs.get("pause_seconds", 0.45))
        target_duration = inputs.get("target_duration_seconds")
        if not 0.5 <= rate <= 2.0 or not 0.8 <= pitch_scale <= 1.2:
            raise ValueError("rate or pitch_scale is outside the supported range")

        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        with tempfile.TemporaryDirectory(prefix="gtts_tts_") as temp_dir:
            raw_path = Path(temp_dir) / "raw.mp3"
            gTTS(text=text, lang=str(inputs.get("lang", "fr")), slow=bool(inputs.get("slow", False))).save(str(raw_path))

            # atempo is pitch-preserving; the preceding sample-rate shift adds a
            # subtle lower register while the adjusted atempo keeps net rate exact.
            tempo_after_pitch = rate / pitch_scale
            filters = [
                f"asetrate={round(44100 * pitch_scale)}",
                "aresample=44100",
                f"atempo={tempo_after_pitch:.6f}",
            ]
            if pause_seconds:
                delay_ms = round(pause_seconds * 1000)
                filters.extend([f"adelay={delay_ms}:all=1", f"apad=pad_dur={pause_seconds:.3f}"])
            if target_duration is not None:
                target_duration = float(target_duration)
                if not 1.0 <= target_duration <= 600.0:
                    raise ValueError("target_duration_seconds must be between 1 and 600")
                filters.append(f"apad=whole_dur={target_duration:.3f}")
            filters.append("loudnorm=I=-18:TP=-1.5:LRA=7")
            cmd = [
                ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw_path),
                "-af", ",".join(filters), "-codec:a", "libmp3lame", "-b:a", "128k",
                "-ar", "44100", str(output_path),
            ]
            subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=180)

        if not output_path.is_file() or output_path.stat().st_size == 0:
            raise RuntimeError("FFmpeg did not create a non-empty MP3")
        return ToolResult(
            success=True,
            data={
                "provider": "gtts",
                "lang": inputs.get("lang", "fr"),
                "slow": bool(inputs.get("slow", False)),
                "voice_style": inputs.get("voice_style", "calm"),
                "requested_voice_identity": "none; Henri-like delivery is simulated",
                "rate": rate,
                "pitch_scale": pitch_scale,
                "pause_seconds": pause_seconds,
                "target_duration_seconds": target_duration,
                "text_length": len(text),
                "output": str(output_path),
                "format": "mp3",
            },
            artifacts=[str(output_path)],
            model="gTTS fr; locally slowed and pitch-shifted",
        )
