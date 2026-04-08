from math_solver import solve
from ai_engine import generate

historial = {}

def detectar_modo(texto):
    t = texto.lower()

    if any(x in t for x in ["triste", "ansioso", "deprimido"]):
        return "psicologo"

    if any(x in t for x in ["dolor", "enfermo", "síntoma"]):
        return "medico"

    if any(x in t for x in ["ley", "policia", "derecho", "legal"]):
        return "legal"

    if any(x in t for x in ["organizar", "agenda", "tareas"]):
        return "organizador"

    return "normal"

def process(user, message):

    # 🧮 matemáticas primero
    mate = solve(message)
    if mate:
        return mate

    modo = detectar_modo(message)

    if user not in historial:
        historial[user] = []

    historial[user].append({"role": "user", "content": message})

    respuesta = generate(historial[user], modo)

    historial[user].append({"role": "assistant", "content": respuesta})

    return respuesta