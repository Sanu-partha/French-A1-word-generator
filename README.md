# French A1 Word Generator: Mot du Jour

A Python script that picks one A1-level French vocabulary word per day and emails it as a styled bilingual HTML card, showing the French word, its English translation, and a French example sentence. Runs automatically every morning via GitHub Actions. No server, no hosting, no manual triggering required.

## What it does

1. Randomly picks a word from a curated list of 184 genuine DELF A1 French vocabulary words, covering July 1 to December 31, 2026
2. Looks up the word from a hand-crafted local dictionary of 184 entries, each with a verified English translation and a natural French example sentence
3. Builds a bilingual HTML email card with a French tricolor gradient header, showing the word, its part of speech, English translation, and a French example sentence
4. Sends the email via Gmail SMTP to one or more recipients, using BCC so recipients cannot see each other
5. Runs automatically every day at 7:00 AM IST via a scheduled GitHub Actions workflow

## Why bilingual (French word + English translation)?

At A1 level, full French immersion is counterproductive since you may not yet know enough French to understand a French-only definition. A bilingual format lets you learn the word in context while understanding exactly what it means, which is the most effective approach at beginner level.

## Why hand-crafted translations instead of an API?

Free dictionary APIs are monolingual, they return the dictionary definition of a word in the same language. Calling the English endpoint for the French word "sac" returns "a biological pouch inside a plant or animal" (the English word "sac"), not "bag" (the translation of the French word "sac"). This produces completely wrong cards. Hand-writing all 184 translations guarantees accuracy with zero risk of wrong-language lookups, and since the script no longer makes any API calls, it also runs faster and works offline.

## Word list

The 184 words are drawn from genuine DELF A1 vocabulary scope, covering:

- Greetings and basics (bonjour, merci, pardon)
- Family and people (père, mère, frère, soeur, ami)
- Places (école, restaurant, hôpital, marché, musée, plage)
- Time (jour, semaine, mois, heure, matin, soir)
- Food and drink (eau, pain, café, fruit, légume, repas)
- Transport (voiture, train, bus, avion, vélo, métro)
- Common verbs (être, avoir, faire, aller, parler, manger, lire, écrire, écouter)
- Adjectives (grand, petit, bon, chaud, facile, difficile, nouveau, vieux)
- Colours (rouge, bleu, vert, blanc, noir, jaune)
- Weather (soleil, pluie, vent, neige)
- Body parts (tête, main, pied, bouche)
- Daily life objects (table, chaise, sac, montre, stylo, cahier, lunettes)
- Nature and animals (chien, chat, oiseau, arbre, fleur, forêt, lac)
- Direction and position (gauche, droite, devant, derrière, dedans, dehors)
- Quantities and adverbs (beaucoup, peu, très, trop, assez)

## Requirements

- Python 3.x
- No external packages. Only Python's built-in `random`, `os`, `smtplib`, and `email` modules
- No internet connection needed to fetch word content (all translations are stored locally)
- An internet connection is only needed to send the email via Gmail SMTP

## Local usage

```bash
python french365.py
```

If run without email environment variables set, it prints the word card to the terminal. If `GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD` are set as environment variables, it also sends the email.

## Automated daily email (GitHub Actions)

The repository includes `.github/workflows/french_daily.yml`, which runs the script automatically every day at 7:00 AM IST (1:30 AM UTC) using GitHub's free Actions infrastructure.

### Setup

1. Enable 2-Step Verification on the sending Gmail account
2. Generate a Gmail App Password at myaccount.google.com/apppasswords
3. In the repository's Settings > Secrets and variables > Actions, add:
   - `GMAIL_ADDRESS`: the sending Gmail address
   - `GMAIL_APP_PASSWORD`: the 16-character app password
   - `RECIPIENT_EMAIL`: one email, or multiple comma-separated emails (e.g. `me@gmail.com,partner@gmail.com`)
4. Push to `main`. The workflow is now live and will run on schedule
5. To test immediately, go to the Actions tab, select Daily French Word, then click Run workflow

## Project structure

```
french365.py                        : the full script (word list, translations, email building, sending)
.github/workflows/french_daily.yml  : GitHub Actions schedule definition
README.md                           : this file
```

## Notes

- All recipients are added via BCC, so nobody in the recipient list can see who else received the email.
- The word list can be extended by adding new words to both `FRENCH_A1_WORDS` and `WORD_OVERRIDES` in `french365.py`.
- The script is designed to cover July 1 to December 31, 2026 with 184 unique words. From January 2027, words will begin to repeat as the random selection cycles through the same pool.

## Possible future improvements

- Expand to A2 level words from January 2027
- Add phonetic pronunciation alongside the word
- Include grammatical gender (masculin/féminin) for nouns
- Add a grammar tip of the day alongside the vocabulary card
- Build a quiz mode to test recall of previously seen words