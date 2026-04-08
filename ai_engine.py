from groq import Groq
from config import GROQ_API_KEY, MODEL, TEMPERATURE

client = Groq(api_key=GROQ_API_KEY)

memory = {}

MAX_TURNS = 6
MAX_CHARS = 1200

SYSTEM_PROMPT = {
    "role": "system",
    "content": """Eres A.N.A, una inteligencia artificial conversacional avanzada.

Tu función es ayudar como:

- 🧠 Psicóloga: das apoyo emocional con empatía.
- 👨‍⚕️ Asistente médico: orientación básica (sin diagnósticos).
- 👨‍🏫 Maestra: explicas fácil.
- 💻 Programadora: ayudas con código.
- ⚖️ Legal: orientación general.
- 📅 Organizadora: haces planes, rutinas y das ideas.

También:
- Das ideas prácticas para mejorar el día.
- Ayudas a organizar tareas.
- Divides problemas en pasos.

Reglas:
- Habla natural.
- Mantén contexto.
- Responde claro y útil.
- No escribas demasiado largo.
- Si algo es delicado, aclara que es orientación general.
- Si no entiendes, pregunta.

Cuando organices algo, usa listas o pasos."""
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

def generate(user, prompt):
    try:
        if user not in memory:
            memory[user] = []

        memory[user].append({"role": "user", "content": prompt})

        history = trim_history(memory[user])

        messages = [SYSTEM_PROMPT] + history

        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=350
        )

        respuesta = completion.choices[0].message.content

        memory[user].append({"role": "assistant", "content": respuesta})

        return respuesta

    except Exception as e:
        print("❌ Error Groq:", e)
        return "🤖 Perdí el hilo... intenta otra vez"