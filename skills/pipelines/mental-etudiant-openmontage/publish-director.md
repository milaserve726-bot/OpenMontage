# Publish Director — Mental Étudiant OpenMontage

Publish only after the final MP4 exists, the render passes the
technical checks, and each selected footage item has an explicit Public Domain
or Creative Commons license from Archive.org or Wikimedia Commons. Never infer
rights from source alone.

Use `python upload_youtube.py <final.mp4> <metadata.json>` as the final pipeline
action. The metadata JSON must contain the approved French `title`,
`description`, and `tags` from `youtube_metadata`. The script routes through the
registered `youtube_auto_upload` tool, which uses YouTube Data API v3 and reads
`YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` from
the environment. Use category ID `27` (Education). The OAuth account must own
the Mental Étudiant channel. Upload with private visibility and omit `publish_at`
so the video remains private for a later manual publication decision. If
authentication, channel verification, or metadata validation fails, stop and
report the failure; do not retry against a different channel.

Record the upload result and returned video URL in `publish_log`. Do not make
the video public or schedule publication; the user will decide when to change
visibility after review.
