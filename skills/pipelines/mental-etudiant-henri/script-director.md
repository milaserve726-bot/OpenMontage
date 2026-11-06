# Mental Étudiant / Henri — Script Director

## Inputs

Read `TOPIC` from `pipeline_defs/mental_etudiant_henri.py`. Write in French for
students in France, girls and boys, using a calm, grounded, encouraging voice. Cover revision,
exams, concentration, memory, motivation, organization, partiels, bac, or university life as relevant. Avoid clinical diagnosis or
promises of guaranteed academic success.

## Required script shape

1. **Hook — about 30 seconds:** begin with a recognizable student moment, then
   offer a small reason to keep listening. Avoid greetings and clickbait claims.
2. **Five chapters:** give each a clear title, one main idea, a practical example,
   and a gentle transition to the next. Keep the advice specific and achievable.
3. **Conclusion:** recap the central idea and offer one low-pressure action for
   today. Close warmly without guilt or a hard sell.

For the normal long-form mode, the spoken French narration must contain
1100–1200 words (headings excluded), intended to land at 8 minutes
at a measured pace. A test project may explicitly set
`metadata.test_scope="one-minute-demo"`; that mode uses 90–120 words and a
60-second composition. Count the words before submitting. If the count is
outside the active mode's range, revise the script rather than asking TTS to rush.

## Channel identity

- Background: `#0F0F0F`
- Main text: `#FFFFFF`
- Accent: `#FFD700`
- Minimal composition, deliberate line breaks, generous negative space, and
  restrained movement. Use the yellow accent for a small number of key words,
  chapter labels, or progress marks.

## Narration target

The approved configuration is **gTTS**, language `fr`, `slow=False`, with the
requested calm Henri-like style simulated in post: rate `0.85`, pitch scale
`0.97`, and `0.45s` pauses. gTTS does not expose named voice identity, timbre, or
emotion controls; describe Henri as a style target, never as the actual speaker.

## YouTube package

Always generate exactly three distinct, powerful French title options for
students in France, then select the strongest and keep it faithful to the video.
Use simple emotional language and curiosity; avoid bland or overly academic
titles. Strong openings may include “Change ta vie”, “Deviens”, “Arrête”,
“Le secret” or “Personne ne te dit”, without misleading promises. Write the
description in French for students in France. Include exactly three short French
thumbnail text ideas (2–5 words each) that match the selected title, with a
clean, motivating student-focused visual and large readable
French text.

## Review

Confirm the five-chapter structure, word count, French fluency, non-judgmental
tone, and consistency between the title, script, description, and thumbnails.
