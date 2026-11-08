# Mental Etudiant - Henri Factory - Clean
import argparse
import os

TOPIC = "comprendre et apaiser l'anxiete etudiante"
YOUTUBE_DESCRIPTION = "Tu es etudiant et tu te sens stresse ? Cette video t'aide a comprendre."
CHANNEL = "Mental Etudiant"
LANGUAGE = "fr-FR"
TARGET_DURATION_MINUTES = (6, 8)

STRUCTURE = [
    "Hook - 30s",
    "Chapitre 1",
    "Chapitre 2",
    "Chapitre 3",
    "Chapitre 4",
    "Conclusion"
]

VOICE = {
    "provider": "gtts",
    "lang": "fr",
    "delivery": "calme, measured, inner-pitched, Henri style",
    "rate": 0.92,
    "pitch_scale": 0.93,
    "pause_seconds": 0.45,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='')
    args = parser.parse_args()
    print(f"Running Henri factory: {TOPIC} | config: {args.config}")
    os.makedirs("output", exist_ok=True)
    with open("output/test.txt", "w", encoding="utf-8") as f:
        f.write(f"Henri factory OK - {TOPIC}")
    print("Factory OK")

if __name__ == "__main__":
    main()
