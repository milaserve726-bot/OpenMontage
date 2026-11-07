import os, random, glob
from PIL import Image, ImageDraw
from moviepy import ColorClip, TextClip, CompositeVideoClip, concatenate_videoclips

# 1 - مواضيع فرنسية - بلا نقطتين باش ما يخربقش YAML
topics = [
  "Stress Examen - Reste Concentre",
  "Concentration Profonde - Methode Etudiant",
  "Memoire - Retiens Tout Facilement",
  "Revision - 5 Secrets Pour Reussir",
  "Motivation Etude - Ne Abandonne Pas",
  "Sommeil Etudiant - Dors Mieux",
  "Organisation - Plan Parfait",
  "Confiance - Tu Peux Reussir"
]
topic = random.choice(topics)
print(f"TOPIC DU JOUR - {topic}")

# 2 - المصنع يولد 68 مقطع ديال 8 ثواني = 544 ثانية = 9 دقايق
clips = []
for i in range(68):
    color = (random.randint(0,40), random.randint(0,60), random.randint(60,120))
    clip = ColorClip(size=(1280,720), color=color, duration=8)
    clips.append(clip)
    print(f"Clip {i+1}/68 - 8s OK")

final = concatenate_videoclips(clips, method="compose")
final.write_videofile("final_video_9min.mp4", fps=24, codec="libx264", audio=False)
print("VIDEO 9MIN OK")

# 3 - Thumbnail 1280x720
im = Image.new('RGB', (1280,720), (10,10,10))
d = ImageDraw.Draw(im)
d.rectangle([0,0,1280,720], fill=(15,15,40))
d.text((80,220), "MENTAL ETUDIANT", fill=(250,204,21))
d.text((80,330), topic, fill=(255,255,255))
d.text((80,550), "9 MIN - METHODE POUR REUSSIR", fill=(255,255,255))
im.save("thumbnail.jpg")
print("THUMBNAIL OK")

# 4 - عنوان + وصف + هاشتاغات فرنسي
title = f"{topic} - Methode Mental Etudiant"
desc = f"""{topic}

Tu stresses avant ton examen ? Dans cette video de 9 minutes, tu vas apprendre comment rester concentre, memoriser plus vite et reussir ton examen sans stress.

Abonne-toi a Mental Etudiant pour reussir tes etudes.

#MentalEtudiant #StressExamen #ReussirExamen #Concentration #Etudiant #Revision #MotivationEtude"""
open("title.txt","w",encoding="utf-8").write(title)
open("description.txt","w",encoding="utf-8").write(desc)
print(f"TITLE - {title}")

# 5 - رفع اوتوماتيك
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

creds = Credentials(None, refresh_token=os.environ.get("YOUTUBE_REFRESH_TOKEN"), client_id=os.environ.get("YOUTUBE_CLIENT_ID"), client_secret=os.environ.get("YOUTUBE_CLIENT_SECRET"), token_uri="https://oauth2.googleapis.com/token")
creds.refresh(Request())
youtube = build("youtube", "v3", credentials=creds)
body = {"snippet": {"title": title, "description": desc, "tags": ["Mental Etudiant","Stress Examen","Reussir Examen","Concentration","Etudiant"], "categoryId": "27", "defaultLanguage": "fr", "defaultAudioLanguage": "fr"}, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}
media = MediaFileUpload("final_video_9min.mp4", chunksize=-1, resumable=True)
resp = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
print("UPLOADED TO YOUTUBE -", resp["id"])
youtube.thumbnails().set(videoId=resp["id"], media_body=MediaFileUpload("thumbnail.jpg")).execute()
print("THUMBNAIL UPLOADED - FACTORY TERMINE")
