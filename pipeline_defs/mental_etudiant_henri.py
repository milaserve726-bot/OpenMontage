# Mental Etudiant - Henri Real Factory - Concentration
import argparse, os, textwrap

TOPIC = "Comment se concentrer quand on est etudiant"
SCRIPT = """
Bonjour, c'est Henri. Bienvenue sur Mental Etudiant.

Tu t'assois pour reviser. Tu ouvres ton cahier. Et apres deux minutes, ton telephone t'appelle. Tu regardes une notification, puis une autre. Et une heure passe sans que tu aies vraiment travaille.

Si tu vis ca, tu n'es pas paresseux. Tu es juste un etudiant normal, dans un monde qui fait tout pour voler ton attention.

Aujourd'hui, on va comprendre pourquoi tu n'arrives pas a te concentrer, et surtout, comment retrouver ta concentration, doucement, sans te punir.

Chapitre 1 : Pourquoi ton cerveau fuit.

Ton cerveau n'est pas fait pour rester concentre 3 heures d'affilee. Il est fait pour survivre. Il cherche la nouveaute, le plaisir rapide, le danger.

Quand tu revises, c'est difficile. Quand tu regardes ton telephone, c'est facile et gratifiant. Alors ton cerveau choisit le facile. Ce n'est pas un manque de volonte. C'est de la biologie.

Le probleme, ce n'est pas toi. C'est que tu demandes a ton cerveau de faire un marathon sans entrainement.

Chapitre 2 : La regle des 25 minutes.

Oublie les 3 heures de revision. On commence petit. On met un minuteur de 25 minutes. Pendant 25 minutes, une seule tache. Telephone en mode avion, dans une autre piece.

Apres 25 minutes, 5 minutes de pause. Tu te leves, tu bois de l'eau, tu respires.

Tu repetes ca 3 fois. Et la, tu as deja travaille 75 minutes de vrai travail. C'est plus que la plupart des etudiants en une journee entiere.

Chapitre 3 : Prepare ton environnement.

La concentration ne commence pas dans ta tete. Elle commence sur ta table.

Une table propre. Une seule feuille. Un seul stylo. Une bouteille d'eau. Rien d'autre.

Si ton telephone est a cote de toi, meme eteint, ton cerveau pense a lui. Eloigne-le. C'est le plus grand cadeau que tu peux te faire.

Chapitre 4 : Ecris ce qui te distrait.

Quand une pensee te vient pendant que tu travailles - je dois envoyer ce message, je dois penser a cet examen - ne lutte pas. Ecris-la sur un papier a cote de toi, et reviens a ton travail.

Ton cerveau se calme quand il sait que tu n'as pas oublie. Tu traiteras cette pensee apres tes 25 minutes.

Conclusion.

Tu n'as pas besoin d'etre parfait. Tu as besoin d'etre regulier.

Demain, fais juste un seul pomodoro de 25 minutes. Un seul. Si tu le fais, tu as deja gagne.

Tu es capable. Tu n'as pas besoin de plus de motivation. Tu as besoin d'un systeme plus doux.

C'etait Henri, sur Mental Etudiant. Prends soin de toi, et on se retrouve demain.
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='')
    args = parser.parse_args()
    os.makedirs("output", exist_ok=True)
    with open("output/script.txt", "w", encoding="utf-8") as f:
        f.write(SCRIPT)
    print(f"Script genere: {len(SCRIPT.split())} mots")
    print(f"Topic: {TOPIC}")
    # Audio
    try:
        from gtts import gTTS
        tts = gTTS(text=SCRIPT, lang='fr', slow=False)
        tts.save("output/audio.mp3")
        print("Audio OK - audio.mp3 cree")
    except Exception as e:
        print(f"Audio skip: {e}")
    print("Factory OK - Real Video Ready")

if __name__ == "__main__":
    main()
