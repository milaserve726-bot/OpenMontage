from google_auth_oauthlib.flow import InstalledAppFlow
import os
from dotenv import load_dotenv
load_dotenv()
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": os.getenv("YOUTUBE_CLIENT_ID"),
            "client_secret": os.getenv("YOUTUBE_CLIENT_SECRET"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"]
        }
    },
    SCOPES
)
creds = flow.run_local_server(port=0)
print("REFRESH_TOKEN:")
print(creds.refresh_token)
