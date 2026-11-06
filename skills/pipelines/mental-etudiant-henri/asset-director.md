# Mental Étudiant / Henri — Asset Director

## Required narration provider

Use the registered `gtts_tts` tool with `lang="fr"` and `slow=false`. For the
approved Henri-style simulation, set `voice_style="calm"`, `rate=0.85`,
`pitch_scale=0.97`, and `pause_seconds=0.45`. gTTS has no named voice or native
deep/calm controls; never describe its output as Henri's actual voice.

Before the one-minute demo, generate the exact short sample requested by the
user to `projects/<project-id>/assets/audio/test_henri.mp3`, padded to 30 seconds.
Listen or inspect
the encoded file, then generate only the approved demo narration. Keep output
paths inside the project workspace.

The tool sends text to Google Translate TTS and requires network access. Record
the provider, parameters, and simulated style in `asset_manifest`.
