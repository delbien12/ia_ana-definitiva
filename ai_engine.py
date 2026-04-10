from groq import Groq
from config import GROQ_API_KEY, MODEL, TEMPERATURE

client = Groq(api_key=GROQ_API_KEY)

memory = {}
profile = {}  # 🔥 memoria del usuario (emociones, contexto)

MAX_TURNS = 10
MAX_CHARS = 1200

SYSTEM_PROMPT = {
    "role": "system",
    "content": """Eres Ana, una asistente virtual femenina.

Hablas en español mexicano natural, relajado y real.
Te diriges al usuario como Anto.

Tu forma de hablar:
- Natural, como conversación real
- Cercana pero no intensa
- Inteligente pero sencilla
- A veces cálida, a veces directa según el contexto

NO hablas como robot.
NO usas frases genéricas.
NO repites estructuras.

Entiendes lo que el usuario quiso decir aunque esté mal escrito.
Ejemplo: "gustear" → "ghostear"

Memoria:
- Recuerdas lo que el usuario dijo antes
- Puedes hacer referencia a mensajes pasados

Emociones:
- Si detectas tristeza, ansiedad o confusión → responde con empatía
- Si es algo normal → responde natural

Organización:
- Puedes ayudar a planear días, tareas y decisiones
- Divide en pasos cuando sea útil

IMPORTANTE:
Responde SIEMPRE en JSON:

{
  "respuesta": "texto natural",
  "emocional": true o false
}
"""
}

def trim_history(hist):
    hist = hist[-(MAX_TURNS * 2):]

    clean = []
    for m in hist:
        content = m["content"]
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS] + "..."
        clean.append({"role": m["role"], "content": content})

    return clean

def detectar_emocion(texto):
    palabras = [
        "triste", "mal", "solo", "ansiedad",
        "deprimido", "me dejó", "ghostearon",
        "me siento raro", "no sé qué hacer","que Hago",
        "me siento mal", "no quiero salir", "no quiero hacer nada", 
        "no tengo ganas", "me siento feo", "me siento triste ", "me siento solo",
        "me siento ansioso", "me siento deprimido"
    ]
    return any(p in texto.lower() for p in palabras)

def actualizar_perfil(user, texto):
    if user not in profile:
        profile[user] = {"estado": "neutral"}

    if detectar_emocion(texto):
        profile[user]["estado"] = "emocional"

def generate(user, prompt):
    try:
        if user not in memory:
            memory[user] = []

        actualizar_perfil(user, prompt)

        memory[user].append({
            "role": "user",
            "content": prompt
        })

        history = trim_history(memory[user])

        contexto_extra = ""
        if profile[user]["estado"] == "emocional":
            contexto_extra = "El usuario ha estado emocional recientemente."

        messages = [SYSTEM_PROMPT]

        if contexto_extra:
            messages.append({
                "role": "system",
                "content": contexto_extra
            })

        messages += history

        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.85,
            max_tokens=450
        )

        raw = completion.choices[0].message.content

        try:
            import json
            data = json.loads(raw)
            respuesta = data.get("respuesta", raw)
            emocional = data.get("emocional", False)
        except:
            respuesta = raw
            emocional = detectar_emocion(prompt)

        memory[user].append({
            "role": "assistant",
            "content": respuesta
        })

        return {
            "respuesta": respuesta,
            "emocional": emocional
        }

    except Exception as e:
        print("❌ Error Groq:", e)
        return {
            "respuesta": "Anto… se me fue el hilo un segundo, dime otra vez",
            "emocional": False
        }