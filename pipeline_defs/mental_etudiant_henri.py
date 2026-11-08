# Mental Etudiant - Henri Real Factory - OpenMontage
# HAD L-MASNAA3 KAYDIR KOLCHI: Video + Thumbnail + Title + Description + Hashtags + Audio

import os
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import subprocess
import textwrap

os.makedirs("output", exist_ok=True)

# 1. TOPIC + TITLE + DESCRIPTION + HASHTAGS
TOPIC = "Comment se concentrer quand on est etudiant"
TITLE = "Comment Se Concentrer Quand On Est Etudiant | 3 Regles Qui Changent Tout"
DESCRIPTION = """Tu n'arrives pas a te concentrer pour reviser ? Tu n'es pas paresseux, tu as juste besoin d'une methode.

Dans cette video, je te donne 3 regles simples pour te concentrer 25 minutes, sans telephone, sans stress, et reviser efficacement.

⏱️ Chapitres:
0:00 Intro - Pourquoi tu n'arrives pas a te concentrer
1:00 Regle 1 - La regle des 25 minutes
3:00 Regle 2 - Le telephone loin de toi
5:00 Regle 3 - Ecris ce qui te distrait

Abonne-toi a Mental Etudiant pour plus de videos sur la concentration, la motivation et les etudes.

#MentalEtudiant #Concentration #Etudiant #Revision #Motivation #Etudes #Focus #Productivite"""

HASHTAGS = "#MentalEtudiant #Concentration #Etudiant #Revision #Motivation #Etudes #Focus #Productivite #ConseilsEtudiant #ReussirSesEtudes"

# 2. SCRIPT HENRI
SCRIPT = """Bonjour, c'est Henri. Bienvenue sur Mental Etudiant.

Ecoute-moi, si tu n'arrives pas a te concentrer, tu n'es pas paresseux. Tu as juste besoin d'une methode.

Chapitre 1. Pourquoi tu n'arrives pas a te concentrer.

Ton cerveau n'est pas fait pour rester concentre 3 heures. Il cherche la facilite. Quand tu revises, c'est dur. Quand tu prends ton telephone, c'est facile. Donc ton cerveau va vers le facile. C'est normal.

Chapitre 2. La regle des 25 minutes.

Tu vas travailler 25 minutes, sans telephone, sans musique avec paroles, sans rien. Apres 25 minutes, tu fais une pause de 5 minutes. Tu repetes ca 3 fois. Tu as deja travaille 75 minutes de vrai travail.

Chapitre 3. Ton telephone est ton ennemi.

Si ton telephone est a cote de toi, tu vas le regarder. Mets-le dans une autre piece. Mets-le en mode avion. Ton telephone peut attendre, tes etudes ne peuvent pas attendre.

Conclusion. Tu n'as pas besoin d'etre parfait. Tu as besoin d'etre regulier. Demain, fais juste un pomodoro de 25 minutes. Un seul. Si tu le fais, tu es deja en train de changer.

C'etait Henri, sur Mental Etudiant. Prends soin de toi."""

# 3. SAVE TEXT FILES
with open("output/script.txt", "w", encoding="utf-8") as f:
    f.write(SCRIPT)
with open("output/title.txt", "w", encoding="utf-8") as f:
    f.write(TITLE)
with open("output/description.txt", "w", encoding="utf-8") as f:
    f.write(DESCRIPTION)
with open("output/hashtags.txt", "w", encoding="utf-8") as f:
    f.write(HASHTAGS)
print(f"Script genere: {len(SCRIPT.split())} mots")
print(f"Titre OK: {TITLE}")
print(f"Description OK + Hashtags OK")

# 4. AUDIO HENRI
try:
    tts = gTTS(text=SCRIPT, lang='fr', slow=False)
    tts.save("output/audio.mp3")
    print("Audio OK - audio.mp3 cree")
except Exception as e:
    print(f"Audio skip: {e}")

# 5. THUMBNAIL 1280x720
try:
    img = Image.new('RGB', (1280, 720), color=(10, 10, 40))
    draw = ImageDraw.Draw(img)
    # Titre grand
    title_lines = textwrap.wrap("COMMENT SE CONCENTRER ?", width=18)
    y = 180
    for line in title_lines:
        draw.text((80, y), line, fill=(255, 220, 0))
        y += 110
    draw.text((80, 480), "3 REGLES QUI CHANGENT TOUT", fill=(255, 255, 255))
    draw.text((80, 580), "MENTAL ETUDIANT - HENRI", fill=(0, 200, 255))
    img.save("output/thumbnail.jpg")
    print("Thumbnail OK - thumbnail.jpg cree")
except Exception as e:
    print(f"Thumbnail skip: {e}")

# 6. VIDEO - Image + Audio
try:
    cmd = ["ffmpeg", "-y", "-loop", "1", "-i", "output/thumbnail.jpg", "-i", "output/audio.mp3", "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", "output/video.mp4"]
    subprocess.run(cmd, check=True)
    print("Video OK - video.mp4 cree")
    print("Factory OK - KOLCHI WAJED")
except Exception as e:
    print(f"Video skip: {e}")
