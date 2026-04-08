import re

# memoria simple por usuario
user_warnings = {}

BAD_WORDS = [
    "idiota",
    "estúpido",
    "estupido",
    "tonto",
    "imbécil",
    "imbecil",
    "pendejo",
    "pendeja",
    "mierda",
    "puta",
    "puto",
    "vete a la",
    "callate",
    "cállate",
    "no sirves",
    "eres basura"
]


def detect_disrespect(text):
    text = text.lower()

    for word in BAD_WORDS:
        if re.search(rf"\b{word}\b", text):
            return True

    return False


def handle_user(user, message):

    if user not in user_warnings:
        user_warnings[user] = 0

    if detect_disrespect(message):
        user_warnings[user] += 1

    count = user_warnings[user]

    if count == 1:
        return "⚠️ Por favor mantén el respeto. Estoy aquí para ayudarte."

    elif count == 2:
        return "⚠️ Segunda advertencia. Mantén un lenguaje respetuoso."

    elif count >= 3:
        return "⛔ Se detectaron múltiples faltas de respeto. Continuaré en modo serio."

    return None
