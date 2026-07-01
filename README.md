# French A1 Word Generator: Mot du Jour

A Python script that picks one A1-level French vocabulary word per day, fetches its English translation and a French example sentence using a free dictionary API, and emails it as a styled bilingual HTML card. Runs automatically every morning via GitHub Actions. No server, no hosting, no manual triggering required.

## What it does

1. Randomly picks a word from a curated list of 184 genuine DELF A1 French vocabulary words, covering July 1 to December 31, 2026
2. Fetches the English translation from the Free Dictionary API (English endpoint, no key required)
3. Fetches a French example sentence from the same API (French endpoint)
4. Builds a bilingual HTML email card with a French tricolor gradient header, showing the word, its part of speech, English translation, and a French example sentence
5. Sends the email via Gmail SMTP to one or more recipients, using BCC so recipients cannot see each other
6. Runs automatically every day at 7:00 AM IST via a scheduled GitHub Actions workflow

## Why bilingual (French word + English translation)?

At A1 level, full French immersion (French definition in French) is counterproductive since you may not yet know enough French to understand the definition itself. A bilingual format lets you learn the word in context while still understanding exactly what it means, which is the most effective approach at beginner level.

## Word list

The 184 words are drawn from genuine DELF A1 vocabulary scope, covering:

- Greetings and basics
- Family and people
- Places (school, restaurant, hospital, market)
- Time (day, week, month, year, hour)
- Food and drink
- Transport
- Common verbs (être, avoir, faire, aller, parler, manger, lire, écrire)
- Adjectives (grand, petit, bon, chaud, facile, difficile)
- Colours
- Weather
- Body parts
- Daily life objects (table, chaise, sac, montre, stylo)
- Direction and position (gauche, droite, devant, derrière)
- Nature and animals

## Requirements

- Python 3.x
- An internet connection (the script calls a live API and an SMTP server)
- No external packages. Only Python's built-in `urllib`, `json`, `random`, `os`, `smtplib`, and `email` modules

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
french365.py                      : the full script (word list, API calls, email building, sending)
.github/workflows/french_daily.yml : GitHub Actions schedule definition
README.md                         : this file
```

## Notes

- Some words may have no example sentence available from the French API endpoint. In that case, the card shows a personalized prompt ("Try using the word in a French sentence today!") instead of leaving it blank.
- All recipients are added via BCC, so nobody in the recipient list can see who else received the email.
- The word list can be expanded by simply adding new A1 words to the `FRENCH_A1_WORDS` list in `french365.py`.

## Possible future improvements

- Expand to A2 level words once A1 vocabulary is covered
- Add phonetic pronunciation alongside the word
- Include a grammar note (e.g. gender: masculine/feminine) for nouns
- Add a quiz mode to test recall of previously seen words
