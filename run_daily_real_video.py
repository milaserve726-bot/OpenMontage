import os, datetime, random
from gtts import gTTS

# سكريبت واجد فابور - كيتبدل كل نهار بوحدو
topics = [
    ("3 عادات صغيرة كتبدل حياتك", "أول عادة هي تنوض بكري. تاني عادة تشرب الماء. تالت عادة تقرا 10 دقايق كل نهار. هاد العادات الصغيرة كيديرو فرق كبير مع الوقت. جربهم و شوف الفرق."),
    ("علاش خاصك تبدا اليوم ماشي غدا", "بزاف ديال الناس كيقولو غدا غادي نبدا. ولكن غدا كتولي بعد غدا. الحل هو تبدا بخطوة صغيرة اليوم. خطوة وحدة كافية باش تبدل كلشي."),
    ("كيفاش تحافظ على الطاقة ديالك", "بعد على الناس السلبيين. نعس مزيان. و دير شي حاجة كتحبها كل نهار. الطاقة ديالك هي راس مالك."),
]
today = datetime.date.today().toordinal()
title, script = topics[today % len(topics)]
print(f"Topic: {title}")

# الصوت فابور
tts = gTTS(text=script, lang='ar')
tts.save("voice.mp3")

# الفيديو - غادي يتصايب من الصوت و عنوان
from moviepy import AudioFileClip, ColorClip, TextClip, CompositeVideoClip
audio = AudioFileClip("voice.mp3")
bg = ColorClip(size=(1080,1920), color=(15,15,30), duration=audio.duration)
txt = TextClip(text=title, font_size=70, color='white', size=(900, None), method='caption')
txt = txt.with_position('center').with_duration(audio.duration)
video = CompositeVideoClip([bg, txt]).with_audio(audio)
video.write_videofile("final.mp4", fps=24, codec="libx264", audio_codec="aac")
print("DONE - final.mp4 created")

# إلا كانو مفاتيح YouTube كاينين، غادي يطلع بوحدو
if os.getenv("YOUTUBE_REFRESH_TOKEN"):
    print("YouTube upload ready - will upload via workflow")
