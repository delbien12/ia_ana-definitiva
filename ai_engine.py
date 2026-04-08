from groq import Groq
from config import GROQ_API_KEY, MODEL, TEMPERATURE, MAX_TOKENS

client = Groq(api_key=GROQ_API_KEY)

# memoria por usuario
memory = {}

# 🔒 LIMITE para evitar que truene
MAX_HISTORY = 6

def generate(user, prompt):
    try:
        # crear memoria si no existe
        if user not in memory:
            memory[user] = [
                {
                    "role": "system",
                    "content": """Eres A.N.A, una IA inteligente, clara y conversacional.

Respondes de forma natural y útil.
Puedes ayudar en matemáticas, organización, consejos y apoyo emocional.

No des respuestas extremadamente largas."""
                }
            ]

        # agregar mensaje usuario
        memory[user].append({
            "role": "user",
            "content": prompt
        })

        # 🔥 recortar historial (evita errores)
        memory[user] = memory[user][-MAX_HISTORY:]

        completion = client.chat.completions.create(
            model=MODEL,
            messages=memory[user],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        respuesta = completion.choices[0].message.content

        # guardar respuesta
        memory[user].append({
            "role": "assistant",
            "content": respuesta
        })

        return respuesta

    except Exception as e:
        print("❌ Error Groq:", e)
        return "⚠️ Error con la IA en la nube."