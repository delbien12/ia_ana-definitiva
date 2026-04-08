from math_solver import solve
from ai_engine import generate

def process(user, message):
    # 1️⃣ intentar matemáticas primero
    resultado_mate = solve(message)

    if resultado_mate:
        return resultado_mate

    # 2️⃣ si no es mate → IA
    respuesta = generate(message)

    return respuesta