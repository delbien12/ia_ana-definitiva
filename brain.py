from math_engine import solve
from ai_engine import generate
from medical_engine import detect_medical, medical_response
def detectar_tipo(texto):
    texto = texto.lower()

    # matemáticas
    if any(x in texto for x in ["+", "-", "*", "/", "raiz", "cuadrado", "ecuacion"]):
        return "matematicas"

    # programación
    if any(x in texto for x in ["codigo", "programa", "c++", "python", "java"]):
        return "codigo"
     #Medico
    if any(x in texto for x in["dolor", "fiebre", "tos","gripa", "gripe", "enfermo", "síntomas","sintomas","medicina","medico","doctor","cabeza","estómago","estomago","náusea","nausea", "mareo","vomito","vomitar","diarrea","covid","temperatura"]):
        return "medico"
        
    return "normal"


def process(user, message):

    tipo = detectar_tipo(message)

    # 🧮 MATEMÁTICAS
    if tipo == "matematicas":
        resultado = solve(message)

        if resultado:
            return resultado

    # 🤖 IA (Groq)
    mensajes = [
        {
            "role": "system",
            "content": """
Eres A.N.A., una IA para estudiantes de preparatoria técnica.

Reglas:
- Responde claro y directo
- Matemáticas: resultado rápido
- Programación: da código completo
- Explicaciones: cortas pero claras
"""
        },
        {"role": "user", "content": message}
    ]

    return generate(mensajes, tipo)
