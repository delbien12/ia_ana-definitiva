from math_engine import solve
from ai_engine import generate
import medical_engine

def detectar_tipo(texto):
    texto = texto.lower()
    # Medicina
    if medical_engine.detect_medical(texto):
        return "medico"
        
    # matemáticas
    if any(x in texto for x in ["+", "-", "*", "/", "raiz", "cuadrado", "ecuacion"]):
        return "matematicas"

    # programación
    if any(x in texto for x in ["codigo", "programa", "c++", "python", "java"]):
        return "codigo"
        
    return "normal"
    
    # 🩺 MÉDICO
    if tipo == "medico":
        resultado = medical_engine.medical_response(message)
        if resultado:
            return resultado
            
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
