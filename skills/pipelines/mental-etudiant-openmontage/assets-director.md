# Assets Director — Mental Étudiant OpenMontage

Use OpenMontage `direct_clip_search` with `sources: ["archive_org", "wikimedia"]`,
`kind: "video"`, and `license_filter: "public_domain_or_creative_commons"` only.
This filter fails closed: reject absent, generic, or verification-needed rights
metadata. Search per approved slot, download candidate motion clips, inspect
thumbnails and playback, then select 2–3 distinct usable videos for every scene.
Never accept image results or silently substitute stock from another provider.
Preserve original URL, creator, title, duration, source, and per-item
license/attribution in `asset_manifest`; never infer rights from the archive name.

For narration, prefer Piper only when an installed French model is confirmed;
otherwise use `gtts_tts` with `lang="fr"`, `slow=false`, rate 0.85, pitch
adjustment if supported, and deliberate pauses. Record that gTTS is an Henri-like
style simulation, not a named voice. Select a subtle instrumental music track
only after recording its source and license. Read the configured TTS and music
Layer 3 skills before calling those tools. Inspect every selected visual and
checkpoint the asset manifest at the human approval gate.
