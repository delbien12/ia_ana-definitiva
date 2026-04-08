from math_solver import solve
from ai_engine import generate

def process(user, message):
    try:
        resultado = solve(message)

        if resultado:
            return resultado

        return generate(user, message)

    except Exception as e:
        print("❌ Error en brain:", e)
        return "⚠️ Error procesando mensaje"