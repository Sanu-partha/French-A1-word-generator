import random
import urllib.request
import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

FRENCH_A1_WORDS = [
    "bonjour", "bonsoir", "merci", "pardon", "homme", "femme", "enfant",
    "ami", "famille", "père", "mère", "frère", "soeur", "maison", "école",
    "ville", "rue", "pays", "restaurant", "magasin", "jour", "nuit", "matin",
    "soir", "semaine", "mois", "année", "heure", "eau", "pain", "café",
    "lait", "fruit", "légume", "viande", "repas", "voiture", "train", "bus",
    "avion", "vélo", "métro", "être", "avoir", "faire", "aller", "venir",
    "voir", "savoir", "pouvoir", "vouloir", "parler", "manger", "boire",
    "dormir", "travailler", "habiter", "grand", "petit", "bon", "mauvais",
    "beau", "nouveau", "vieux", "jeune", "chaud", "froid", "facile",
    "difficile", "important", "possible", "livre", "table", "chaise", "porte",
    "fenêtre", "chambre", "cuisine", "argent", "travail", "temps", "vie",
    "monde", "chose", "question", "rouge", "bleu", "vert", "blanc", "noir",
    "jaune", "soleil", "pluie", "vent", "neige", "tête", "main", "pied",
    "bouche", "prix", "billet", "carte", "téléphone", "ordinateur", "lettre",
    "nombre", "beaucoup", "peu", "assez", "très", "trop", "aimer", "prendre",
    "donner", "mettre", "partir", "arriver", "ouvrir", "fermer", "chercher",
    "trouver", "appeler", "jardin", "parc", "marché", "hôpital", "pharmacie",
    "banque", "poste", "église", "musée", "plage", "montagne", "forêt",
    "rivière", "lac", "chien", "chat", "oiseau", "poisson", "fleur", "arbre",
    "herbe", "assiette", "verre", "fourchette", "couteau", "cuillère", "sac",
    "chapeau", "chaussure", "robe", "pantalon", "chemise", "manteau",
    "lunettes", "montre", "clé", "stylo", "papier", "crayon", "cahier",
    "image", "musique", "film", "sport", "jeu", "vacances", "cadeau",
    "fête", "anniversaire", "couleur", "forme", "taille", "poids",
    "gauche", "droite", "devant", "derrière", "dedans", "dehors",
    "lire", "écrire", "écouter",
]

WORD_OVERRIDES = {}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch_url(url):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode())


def fetch_french_example(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/fr/{word}"
    try:
        data = fetch_url(url)
        for meaning_block in data[0].get("meanings", []):
            for definition in meaning_block.get("definitions", []):
                example = definition.get("example")
                if example:
                    return example
        return None
    except Exception:
        return None


def fetch_english_translation(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        data = fetch_url(url)
        for meaning_block in data[0].get("meanings", []):
            block_pos = meaning_block.get("partOfSpeech", "")
            for definition in meaning_block.get("definitions", []):
                meaning = definition.get("definition")
                if meaning:
                    return meaning, block_pos
        return None, ""
    except Exception:
        return None, ""


def get_daily_word(max_attempts=10):
    attempted = set()
    for _ in range(max_attempts):
        candidates = [w for w in FRENCH_A1_WORDS if w not in attempted]
        if not candidates:
            break
        word = random.choice(candidates)
        attempted.add(word)

        if word in WORD_OVERRIDES:
            override = WORD_OVERRIDES[word]
            return {
                "word": word,
                "part_of_speech": override.get("part_of_speech", ""),
                "translation": override.get("translation"),
                "example": override.get("example"),
            }

        translation, part_of_speech = fetch_english_translation(word)
        if translation:
            example = fetch_french_example(word)
            return {
                "word": word,
                "part_of_speech": part_of_speech,
                "translation": translation,
                "example": example,
            }

    return None


def build_word_card_text(details):
    lines = []
    lines.append("=" * 50)
    lines.append(f"  MOT DU JOUR: {details['word'].upper()}")
    lines.append("=" * 50)
    if details["part_of_speech"]:
        lines.append(f"Part of speech : {details['part_of_speech']}")
    lines.append(f"Translation    : {details['translation']}")
    if details["example"]:
        lines.append(f"Example        : \"{details['example']}\"")
    else:
        lines.append(f"Example        : Try using \"{details['word']}\" in a French sentence today!")
    lines.append("=" * 50)
    return "\n".join(lines)


def build_word_card_html(details):
    example_html = (
        f'<p style="margin:0 0 6px 0;"><strong>Example</strong><br>'
        f'<em>"{details["example"]}"</em></p>'
        if details["example"]
        else f'<p style="margin:0 0 6px 0; color:#888;"><strong>Example</strong><br>'
             f'Try using "{details["word"]}" in a French sentence today!</p>'
    )

    pos_html = (
        f'<span style="display:inline-block; background:#eef2ff; color:#4338ca; '
        f'font-size:12px; font-weight:600; padding:4px 10px; border-radius:12px; '
        f'text-transform:uppercase; letter-spacing:0.5px;">{details["part_of_speech"]}</span>'
        if details["part_of_speech"]
        else ""
    )

    html = f"""
    <div style="font-family:'Segoe UI', Arial, sans-serif; max-width:480px; margin:0 auto;
                background:#ffffff; border-radius:16px; overflow:hidden;
                box-shadow:0 4px 16px rgba(0,0,0,0.08); border:1px solid #eee;">
      <div style="background:linear-gradient(135deg,#0055a4,#ef4135); padding:24px 28px;">
        <p style="margin:0; color:#ffffff; font-size:13px; letter-spacing:1px; text-transform:uppercase;">
          Mot du Jour &mdash; French Word of the Day
        </p>
        <h1 style="margin:6px 0 0 0; color:#ffffff; font-size:32px; font-weight:700;">
          {details['word'].capitalize()}
        </h1>
        {pos_html}
      </div>
      <div style="padding:24px 28px;">
        <p style="margin:0 0 16px 0; font-size:15px; color:#1f2937; line-height:1.5;">
          <strong>English Translation</strong><br>{details['translation']}
        </p>
        <div style="font-size:15px; color:#1f2937; line-height:1.5; margin-bottom:16px;">
          {example_html}
        </div>
      </div>
      <div style="background:#f9fafb; padding:14px 28px; text-align:center;">
        <p style="margin:0; font-size:12px; color:#9ca3af;">
          Un mot par jour &mdash; One word a day, building French fluency step by step.
        </p>
      </div>
    </div>
    """
    return html


def print_word_card(details):
    print(build_word_card_text(details))


def send_email(subject, plain_body, html_body):
    sender_email = os.environ["GMAIL_ADDRESS"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient_raw = os.environ.get("RECIPIENT_EMAIL", sender_email)
    recipient_emails = [email.strip() for email in recipient_raw.split(",") if email.strip()]

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = sender_email

    message.attach(MIMEText(plain_body, "plain", "utf-8"))
    message.attach(MIMEText(html_body, "html", "utf-8"))

    all_recipients = list(dict.fromkeys([sender_email] + recipient_emails))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, all_recipients, message.as_string())


if __name__ == "__main__":
    result = get_daily_word()
    if result:
        print_word_card(result)
        if "GMAIL_ADDRESS" in os.environ and "GMAIL_APP_PASSWORD" in os.environ:
            subject = f"Mot du Jour: {result['word'].capitalize()}"
            plain_body = build_word_card_text(result)
            html_body = build_word_card_html(result)
            send_email(subject, plain_body, html_body)
            print("Email sent successfully.")
    else:
        print("Could not fetch a word today — check your internet connection and try again.")