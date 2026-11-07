import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

creds = Credentials(
    None,
    refresh_token=os.getenv("YOUTUBE_REFRESH_TOKEN"),
    token_uri="https://oauth2.googleapis.com/token",
    client_id=os.getenv("YOUTUBE_CLIENT_ID"),
    client_secret=os.getenv("YOUTUBE_CLIENT_SECRET"),
)
youtube = build("youtube", "v3", credentials=creds)
request = youtube.videos().insert(
    part="snippet,status",
    body={"snippet": {"title": "فيديو اليوم - OpenMontage", "description": "فيديو يومي فابور", "categoryId": "22"}, "status": {"privacyStatus": "public"}},
    media_body=MediaFileUpload("final.mp4", chunksize=-1, resumable=True)
)
print(request.execute())
print("UPLOADED TO YOUTUBE")
