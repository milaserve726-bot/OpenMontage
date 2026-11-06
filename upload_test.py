import os, json, sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
# load .env if exists
if os.path.exists('.env'):
    for line in open('.env'):
        if '=' in line and not line.strip().startswith('#'):
            k,v=line.strip().split('=',1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
video_path=sys.argv[1]
meta=json.load(open(sys.argv[2]))
creds=Credentials(None, refresh_token=os.environ['YOUTUBE_REFRESH_TOKEN'], token_uri='https://oauth2.googleapis.com/token', client_id=os.environ['YOUTUBE_CLIENT_ID'], client_secret=os.environ['YOUTUBE_CLIENT_SECRET'])
yt=build('youtube','v3',credentials=creds)
req=yt.videos().insert(part='snippet,status', body={'snippet':{'title':meta['title'],'description':meta['description'],'tags':meta.get('tags',[]),'categoryId':'27'},'status':{'privacyStatus':'private'}}, media_body=MediaFileUpload(video_path))
vid=req.execute()
print('UPLOADED OK videoId=', vid['id'])
