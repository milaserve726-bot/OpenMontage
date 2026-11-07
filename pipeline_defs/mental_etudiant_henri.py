cat > .github/workflows/daily.yml << 'EOF'
name: Daily Video
on:
  schedule:
      - cron: '0 17 * * *'
        workflow_dispatch:
        jobs:
          build:
              runs-on: ubuntu-latest
                  steps:
                        - uses: actions/checkout@v4
                              - uses: actions/setup-python@v5
                                      with:
                                                python-version: '3.11'
                                                      - name: Install deps
                                                              run: pip install moviepy imageio-ffmpeg Pillow gtts google-api-python-client google-auth-oauthlib google-auth-httplib2
                                                                    - name: Run OpenMontage 9min
                                                                            run: python run_daily_real_video.py --duration-seconds 540
                                                                                  - name: Make Thumbnail
                                                                                          run: python -c "from PIL import Image, ImageDraw; im=Image.new('RGB',(1280,720),(10,10,10)); d=ImageDraw.Draw(im); d.text((80,280),'MENTAL ETUDIANT',fill=(250,204,21)); d.text((80,380),'Stress Examen - Reste Concentre',fill=(255,255,255)); im.save('thumbnail.jpg')"
                                                                                                - name: Upload to YouTube
                                                                                                        env:
                                                                                                                  YOUTUBE_CLIENT_ID: ${{ secrets.YOUTUBE_CLIENT_ID }}
                                                                                                                            YOUTUBE_CLIENT_SECRET: ${{ secrets.YOUTUBE_CLIENT_SECRET }}
                                                                                                                                      YOUTUBE_REFRESH_TOKEN: ${{ secrets.YOUTUBE_REFRESH_TOKEN }}
                                                                                                                                              run: python upload.py
                                                                                                                                              EOF
                                                                                                                                              git add .
                                                                                                                                              git commit -m "factory full thumbnail title upload"
                                                                                                                                              git pushusine_mentale.py
                                                                                                                                              """Editable channel brief for the Mental Étudiant long-form pipeline.

Change TOPIC, then ask the OpenMontage agent to run the
``mental_etudiant_henri`` pipeline. Pipeline orchestration stays in its YAML
manifest and stage director instructions; this module is only the topic brief.
"""

TOPIC = "comprendre et apaiser l’anxiété étudiante"

# Starter packaging for the default TOPIC. Regenerate these in the script stage
# whenever TOPIC changes; the stage director requires a topic-specific package.
YOUTUBE_TITLE = "Arrête de laisser l’anxiété décider à ta place"
YOUTUBE_DESCRIPTION = """Tu es étudiante et l’anxiété prend trop de place dans tes journées ? Cette vidéo t’aide à comprendre ce qui se passe et à retrouver quelques repères pour avancer avec plus de calme et de confiance. Des pistes simples, pensées pour ton quotidien d’étudiante, sans pression ni jugement.

Ces pistes sont des conseils généraux de bien-être, pas un diagnostic ni un traitement. Elles ne fonctionnent pas de la même façon pour tout le monde. Si l’anxiété pèse sur ton quotidien, parle-en à une personne de confiance ou à un professionnel de santé.

#MentalEtudiant #Anxiete #Etudiants #BienEtreEtudiant #SanteMentale"""
THUMBNAIL_TEXT_IDEAS = (
    "TON CERVEAU EN ALERTE ?",
    "L’ANXIÉTÉ, ON EN PARLE",
    "5 PORTES POUR SOUFFLER",
)

CHANNEL = "Mental Étudiant"
LANGUAGE = "fr-FR"
TARGET_DURATION_MINUTES = (8, 8)
SCRIPT_WORDS = (1100, 1200)

STRUCTURE = (
    "Hook ~30s",
    "Chapitre 1",
    "Chapitre 2",
    "Chapitre 3",
    "Chapitre 4",
    "Chapitre 5",
    "Conclusion",
)

VOICE = {
    "provider": "gtts",
    "name": "Henri-style (simulated; gTTS has no named voice selection)",
    "lang": "fr",
    "slow": False,
    "delivery": "calm, measured, lower-pitched; Henri style is simulated",
    "rate": 0.85,
    "pitch_scale": 0.97,
    "pause_seconds": 0.45,
}

VISUALS = {
    "background": "#0F0F0F",
    "text": "#FFFFFF",
    "accent": "#FFD700",
    "style": "minimal",
}
TITLE_GENERATION = {
    "language": "fr",
    "audience": "étudiants et étudiantes en France",
    "style": "simple, émotionnel, puissant, curieux et fidèle au contenu; jamais banal ni trompeur",
    "generate": 3,
    "choose_best": True,
    "selected_title": YOUTUBE_TITLE,
    "examples": [
        "Change ta vie d'étudiante en 8 minutes",
        "Le secret des étudiants qui réussissent leurs partiels",
        "Arrête de te saboter, deviens inarrêtable",
        "Comment devenir la meilleure version de toi avant les examens",
    ],
    "power_words": ["Change ta vie", "Deviens", "Arrête", "Le secret", "Personne ne te dit"],
    "rules": "Toujours écrire exactement 3 titres en français, en choisir le plus puissant, et vérifier qu'il correspond au contenu.",
}

THUMBNAIL = {
    "language": "fr",
    "background": "#0F0F0F",
    "main_text": "ARRÊTE DE T'AUTOSABOTER",
    "main_text_color": "#FFD700",
    "sub_text": "Reprends confiance en toi",
    "sub_text_color": "#FFFFFF",
    "style": "propre, motivant et inclusif; étudiant ou étudiante visible; très grand texte français lisible; contraste fort; cohérent avec le titre",
    "size": "1920x1080",
    "auto_generate": True,
}

DESCRIPTION_TEMPLATE = {
    "language": "fr",
    "intro": "Des conseils en français pour les étudiantes et étudiants en France : révisions, concentration, motivation et réussite sans pression.",
    "cta": "Choisis une idée qui te parle et avance à ton rythme.",
    "hashtags": [
        "#MentalEtudiant",
        "#Anxiete",
        "#Etudiants",
        "#BienEtreEtudiant",
        "#SanteMentale",
    ],
    "tags": [
        "mental étudiant",
        "anxiété étudiante",
        "stress étudiant",
        "bien-être étudiant",
        "concentration",
        "révisions examens",
        "partiels fac",
        "bac révisions",
        "mémoire étudiant",
        "organisation études",
        "santé mentale",
    ],
    "auto_generate": True,
}

YOUTUBE_PUBLISH = {
    "enabled": True,
    "channel": "Mental Étudiant",
    "privacy": "public",
    "category": "Education",
    "language": "fr",
    "target_audience": "étudiants et étudiantes en France",
    "duration_minutes": 8,
    "title_options_per_video": 3,
    "select_strongest_title": True,
    "upload_auto": True,
    "publish_daily": True,
    "use_thumbnail": True,
    "use_description": True,
    "use_tags": True,
}
