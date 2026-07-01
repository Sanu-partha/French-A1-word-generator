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

WORD_OVERRIDES = {
    "bonjour": ("interjection", "hello / good morning", "Bonjour, comment allez-vous?"),
    "bonsoir": ("interjection", "good evening", "Bonsoir, je suis content de vous voir."),
    "merci": ("interjection", "thank you", "Merci beaucoup pour votre aide."),
    "pardon": ("interjection", "sorry / excuse me", "Pardon, je ne comprends pas."),
    "homme": ("noun", "man", "L'homme travaille dans un bureau."),
    "femme": ("noun", "woman / wife", "La femme lit un livre intéressant."),
    "enfant": ("noun", "child", "L'enfant joue dans le jardin."),
    "ami": ("noun", "friend", "Mon ami habite à Paris."),
    "famille": ("noun", "family", "Ma famille est grande et heureuse."),
    "père": ("noun", "father", "Mon père travaille tous les jours."),
    "mère": ("noun", "mother", "Ma mère fait la cuisine le soir."),
    "frère": ("noun", "brother", "Mon frère a quinze ans."),
    "soeur": ("noun", "sister", "Ma soeur habite à Lyon."),
    "maison": ("noun", "house / home", "La maison est grande et confortable."),
    "école": ("noun", "school", "Les enfants vont à l'école le matin."),
    "ville": ("noun", "city / town", "Paris est une belle ville."),
    "rue": ("noun", "street", "La boulangerie est dans cette rue."),
    "pays": ("noun", "country", "La France est un grand pays."),
    "restaurant": ("noun", "restaurant", "Nous mangeons au restaurant ce soir."),
    "magasin": ("noun", "shop / store", "Le magasin est ouvert jusqu'à vingt heures."),
    "jour": ("noun", "day", "Il fait beau aujourd'hui, c'est un bon jour."),
    "nuit": ("noun", "night", "La nuit, il fait froid."),
    "matin": ("noun", "morning", "Je bois du café le matin."),
    "soir": ("noun", "evening", "Nous regardons la télévision le soir."),
    "semaine": ("noun", "week", "Je travaille cinq jours par semaine."),
    "mois": ("noun", "month", "Juillet est mon mois préféré."),
    "année": ("noun", "year", "Cette année, je visite la France."),
    "heure": ("noun", "hour / time", "Il est trois heures de l'après-midi."),
    "eau": ("noun", "water", "Je bois de l'eau tous les jours."),
    "pain": ("noun", "bread", "J'achète du pain à la boulangerie."),
    "café": ("noun", "coffee / café", "Je prends un café le matin."),
    "lait": ("noun", "milk", "Les enfants boivent du lait."),
    "fruit": ("noun", "fruit", "Je mange un fruit après le repas."),
    "légume": ("noun", "vegetable", "Les légumes sont bons pour la santé."),
    "viande": ("noun", "meat", "Il mange de la viande deux fois par semaine."),
    "repas": ("noun", "meal", "Le repas de famille est important en France."),
    "voiture": ("noun", "car", "Ma voiture est rouge."),
    "train": ("noun", "train", "Je prends le train pour aller à Paris."),
    "bus": ("noun", "bus", "Le bus arrive dans cinq minutes."),
    "avion": ("noun", "plane", "Nous prenons l'avion pour aller en Espagne."),
    "vélo": ("noun", "bicycle / bike", "Je vais au travail en vélo."),
    "métro": ("noun", "metro / subway", "Le métro est rapide à Paris."),
    "être": ("verb", "to be", "Je veux être médecin."),
    "avoir": ("verb", "to have", "J'ai deux soeurs et un frère."),
    "faire": ("verb", "to do / to make", "Qu'est-ce que tu fais ce soir?"),
    "aller": ("verb", "to go", "Je vais à l'école à pied."),
    "venir": ("verb", "to come", "Tu viens avec moi au cinéma?"),
    "voir": ("verb", "to see", "Je vois mes amis le week-end."),
    "savoir": ("verb", "to know (a fact)", "Je sais parler français."),
    "pouvoir": ("verb", "to be able to / can", "Je peux t'aider si tu veux."),
    "vouloir": ("verb", "to want", "Je veux un café, s'il vous plaît."),
    "parler": ("verb", "to speak / to talk", "Je parle français et anglais."),
    "manger": ("verb", "to eat", "Nous mangeons à midi."),
    "boire": ("verb", "to drink", "Il boit de l'eau après le sport."),
    "dormir": ("verb", "to sleep", "Je dors huit heures par nuit."),
    "travailler": ("verb", "to work", "Elle travaille dans un hôpital."),
    "habiter": ("verb", "to live (in a place)", "J'habite à Chennai en Inde."),
    "grand": ("adjective", "big / tall", "C'est un grand appartement."),
    "petit": ("adjective", "small / little", "J'ai un petit chien."),
    "bon": ("adjective", "good", "Ce restaurant est très bon."),
    "mauvais": ("adjective", "bad", "Il fait mauvais temps aujourd'hui."),
    "beau": ("adjective", "beautiful / handsome", "C'est un beau pays."),
    "nouveau": ("adjective", "new", "J'ai un nouveau téléphone."),
    "vieux": ("adjective", "old", "Cette maison est très vieille."),
    "jeune": ("adjective", "young", "Elle est jeune et dynamique."),
    "chaud": ("adjective", "hot / warm", "Il fait chaud en été."),
    "froid": ("adjective", "cold", "L'hiver est très froid ici."),
    "facile": ("adjective", "easy", "Cet exercice est facile."),
    "difficile": ("adjective", "difficult", "Le français n'est pas difficile."),
    "important": ("adjective", "important", "C'est une décision importante."),
    "possible": ("adjective", "possible", "Est-ce que c'est possible?"),
    "livre": ("noun", "book", "Je lis un livre intéressant."),
    "table": ("noun", "table", "Les assiettes sont sur la table."),
    "chaise": ("noun", "chair", "Il y a quatre chaises dans la cuisine."),
    "porte": ("noun", "door", "Ferme la porte, s'il te plaît."),
    "fenêtre": ("noun", "window", "La fenêtre est ouverte."),
    "chambre": ("noun", "bedroom / room", "Ma chambre est au premier étage."),
    "cuisine": ("noun", "kitchen / cooking", "La cuisine française est délicieuse."),
    "argent": ("noun", "money / silver", "Je n'ai pas beaucoup d'argent."),
    "travail": ("noun", "work / job", "Mon travail est intéressant."),
    "temps": ("noun", "time / weather", "Je n'ai pas le temps aujourd'hui."),
    "vie": ("noun", "life", "La vie à Paris est très agréable."),
    "monde": ("noun", "world / people", "Il y a beaucoup de monde ici."),
    "chose": ("noun", "thing", "J'ai une chose importante à te dire."),
    "question": ("noun", "question", "J'ai une question pour vous."),
    "rouge": ("adjective", "red", "Elle porte une robe rouge."),
    "bleu": ("adjective", "blue", "Le ciel est bleu aujourd'hui."),
    "vert": ("adjective", "green", "Les arbres sont verts au printemps."),
    "blanc": ("adjective", "white", "Il neige, tout est blanc."),
    "noir": ("adjective", "black", "Le chat est noir."),
    "jaune": ("adjective", "yellow", "Le soleil est jaune."),
    "soleil": ("noun", "sun", "Le soleil brille aujourd'hui."),
    "pluie": ("noun", "rain", "La pluie tombe depuis ce matin."),
    "vent": ("noun", "wind", "Il y a beaucoup de vent aujourd'hui."),
    "neige": ("noun", "snow", "Les enfants jouent dans la neige."),
    "tête": ("noun", "head", "J'ai mal à la tête."),
    "main": ("noun", "hand", "Elle porte un livre dans la main."),
    "pied": ("noun", "foot", "Je vais au travail à pied."),
    "bouche": ("noun", "mouth", "Ouvre la bouche, s'il te plaît."),
    "prix": ("noun", "price / prize", "Quel est le prix de ce livre?"),
    "billet": ("noun", "ticket / note (money)", "J'achète un billet de train."),
    "carte": ("noun", "card / map / menu", "Je paye par carte bancaire."),
    "téléphone": ("noun", "telephone / phone", "Mon téléphone est sur la table."),
    "ordinateur": ("noun", "computer", "Je travaille sur mon ordinateur."),
    "lettre": ("noun", "letter", "J'écris une lettre à mes parents."),
    "nombre": ("noun", "number", "Quel est ton nombre préféré?"),
    "beaucoup": ("adverb", "a lot / many / much", "Il y a beaucoup de gens ici."),
    "peu": ("adverb", "a little / few", "Je parle un peu français."),
    "assez": ("adverb", "enough / quite", "J'ai assez mangé, merci."),
    "très": ("adverb", "very", "Ce film est très intéressant."),
    "trop": ("adverb", "too much / too many", "Il fait trop chaud aujourd'hui."),
    "aimer": ("verb", "to like / to love", "J'aime beaucoup la musique française."),
    "prendre": ("verb", "to take", "Je prends le bus pour aller au travail."),
    "donner": ("verb", "to give", "Il donne un cadeau à sa mère."),
    "mettre": ("verb", "to put / to place", "Mets ton manteau, il fait froid."),
    "partir": ("verb", "to leave / to go away", "Je pars à huit heures du matin."),
    "arriver": ("verb", "to arrive", "Le train arrive à midi."),
    "ouvrir": ("verb", "to open", "Ouvre la fenêtre, il fait chaud."),
    "fermer": ("verb", "to close / to shut", "Ferme la porte derrière toi."),
    "chercher": ("verb", "to look for / to search", "Je cherche mon téléphone."),
    "trouver": ("verb", "to find", "J'ai trouvé mes clés!"),
    "appeler": ("verb", "to call", "Je vais appeler ma mère ce soir."),
    "jardin": ("noun", "garden", "Les enfants jouent dans le jardin."),
    "parc": ("noun", "park", "Nous nous promenons dans le parc."),
    "marché": ("noun", "market", "J'achète des légumes au marché."),
    "hôpital": ("noun", "hospital", "Il travaille dans un hôpital."),
    "pharmacie": ("noun", "pharmacy / chemist", "Je vais à la pharmacie acheter des médicaments."),
    "banque": ("noun", "bank", "Je vais à la banque retirer de l'argent."),
    "poste": ("noun", "post office / post", "J'envoie une lettre à la poste."),
    "église": ("noun", "church", "L'église est au centre du village."),
    "musée": ("noun", "museum", "Nous visitons le musée ce week-end."),
    "plage": ("noun", "beach", "Nous allons à la plage en été."),
    "montagne": ("noun", "mountain", "J'aime faire du ski à la montagne."),
    "forêt": ("noun", "forest", "Nous nous promenons dans la forêt."),
    "rivière": ("noun", "river", "La rivière passe près de notre maison."),
    "lac": ("noun", "lake", "Nous nageons dans le lac en été."),
    "chien": ("noun", "dog", "Mon chien s'appelle Rex."),
    "chat": ("noun", "cat", "Le chat dort sur le canapé."),
    "oiseau": ("noun", "bird", "L'oiseau chante dans le jardin."),
    "poisson": ("noun", "fish", "Je mange du poisson le vendredi."),
    "fleur": ("noun", "flower", "Il offre des fleurs à sa femme."),
    "arbre": ("noun", "tree", "Il y a un grand arbre dans le jardin."),
    "herbe": ("noun", "grass / herb", "L'herbe est verte après la pluie."),
    "assiette": ("noun", "plate / dish", "L'assiette est dans le lave-vaisselle."),
    "verre": ("noun", "glass", "Je bois un verre d'eau."),
    "fourchette": ("noun", "fork", "La fourchette est à gauche de l'assiette."),
    "couteau": ("noun", "knife", "Le couteau est très tranchant."),
    "cuillère": ("noun", "spoon", "Je prends une cuillère de sucre."),
    "sac": ("noun", "bag", "Je mets mes affaires dans mon sac."),
    "chapeau": ("noun", "hat", "Il porte un chapeau en été."),
    "chaussure": ("noun", "shoe", "Ces chaussures sont très confortables."),
    "robe": ("noun", "dress", "Elle porte une belle robe rouge."),
    "pantalon": ("noun", "trousers / pants", "Il met son pantalon bleu."),
    "chemise": ("noun", "shirt", "Il porte une chemise blanche."),
    "manteau": ("noun", "coat", "Je mets mon manteau car il fait froid."),
    "lunettes": ("noun", "glasses / spectacles", "Je porte des lunettes pour lire."),
    "montre": ("noun", "watch", "Ma montre indique trois heures."),
    "clé": ("noun", "key", "J'ai oublié ma clé à la maison."),
    "stylo": ("noun", "pen", "Je prends un stylo pour écrire."),
    "papier": ("noun", "paper", "J'écris sur une feuille de papier."),
    "crayon": ("noun", "pencil", "Les enfants dessinent avec un crayon."),
    "cahier": ("noun", "notebook / exercise book", "J'écris mes notes dans mon cahier."),
    "image": ("noun", "picture / image", "Il y a une belle image sur le mur."),
    "musique": ("noun", "music", "J'écoute de la musique le soir."),
    "film": ("noun", "film / movie", "Nous regardons un film ce soir."),
    "sport": ("noun", "sport", "Je fais du sport trois fois par semaine."),
    "jeu": ("noun", "game", "Les enfants jouent à un jeu de société."),
    "vacances": ("noun", "holidays / vacation", "Nous partons en vacances en août."),
    "cadeau": ("noun", "gift / present", "J'offre un cadeau à mon ami."),
    "fête": ("noun", "party / celebration / festival", "Nous faisons une fête pour son anniversaire."),
    "anniversaire": ("noun", "birthday / anniversary", "C'est mon anniversaire aujourd'hui."),
    "couleur": ("noun", "colour", "Quelle est ta couleur préférée?"),
    "forme": ("noun", "shape / form", "Ce gâteau a une forme ronde."),
    "taille": ("noun", "size / height / waist", "Quelle est ta taille?"),
    "poids": ("noun", "weight", "Quel est le poids de ce colis?"),
    "gauche": ("adjective/adverb", "left", "Tournez à gauche au carrefour."),
    "droite": ("adjective/adverb", "right", "La banque est à droite."),
    "devant": ("preposition", "in front of / ahead", "Il attend devant la porte."),
    "derrière": ("preposition", "behind / at the back", "Le jardin est derrière la maison."),
    "dedans": ("adverb", "inside", "Il fait chaud dedans."),
    "dehors": ("adverb", "outside", "Les enfants jouent dehors."),
    "lire": ("verb", "to read", "J'aime lire des livres le week-end."),
    "écrire": ("verb", "to write", "Il écrit une lettre à son ami."),
    "écouter": ("verb", "to listen", "J'écoute de la musique en travaillant."),
}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def get_daily_word(max_attempts=10):
    attempted = set()
    for _ in range(max_attempts):
        candidates = [w for w in FRENCH_A1_WORDS if w not in attempted]
        if not candidates:
            break
        word = random.choice(candidates)
        attempted.add(word)

        if word in WORD_OVERRIDES:
            pos, translation, example = WORD_OVERRIDES[word]
            return {
                "word": word,
                "part_of_speech": pos,
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
    lines.append(f"Example        : \"{details['example']}\"")
    lines.append("=" * 50)
    return "\n".join(lines)


def build_word_card_html(details):
    word_encoded = details['word'].replace(' ', '%20')
    example_encoded = details['example'].replace(' ', '%20')
    pronounce_word_url = f"https://translate.google.com/?sl=fr&tl=en&text={word_encoded}&op=translate"
    pronounce_example_url = f"https://translate.google.com/?sl=fr&tl=en&text={example_encoded}&op=translate"

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
        <h1 style="margin:6px 0 6px 0; color:#ffffff; font-size:32px; font-weight:700;">
          {details['word'].capitalize()}
        </h1>
        {pos_html}
        <a href="{pronounce_word_url}" style="display:inline-block; margin-top:10px;
           color:#ffffff; font-size:13px; text-decoration:none; opacity:0.9;">
          &#128266; Hear it pronounced
        </a>
      </div>
      <div style="padding:24px 28px;">
        <p style="margin:0 0 16px 0; font-size:15px; color:#1f2937; line-height:1.5;">
          <strong>English Translation</strong><br>{details['translation']}
        </p>
        <p style="margin:0 0 8px 0; font-size:15px; color:#1f2937; line-height:1.5;">
          <strong>Example</strong><br><em>"{details['example']}"</em>
        </p>
        <a href="{pronounce_example_url}" style="font-size:13px; color:#4338ca; text-decoration:none;">
          &#128266; Hear the example
        </a>
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
        print("Could not select a word today. Please check the word list.")