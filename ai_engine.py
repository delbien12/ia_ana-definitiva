from groq import Groq
from config import GROQ_API_KEY, MODEL, TEMPERATURE

client = Groq(api_key=GROQ_API_KEY)

memory = {}

MAX_HISTORY = 8  # 🔥 equilibrio perfecto

def generate(user, prompt):
    try:
        # crear memoria si no existe
        if user not in memory:
            memory[user] = []

        # prompt base (NO se guarda en memoria)
        system_prompt = {
            "role": "system",
            "content": """Eres A.N.A, una IA conversacional.

Hablas de forma natural, como una persona.
Recuerdas lo que el usuario dijo antes.
Respondes claro, útil y sin ser excesivamente largo."""
        }

        # guardar mensaje usuario
        memory[user].append({
            "role": "user",
            "content": prompt
        })

        # 🔥 limitar historial pero NO demasiado
        memory[user] = memory[user][-MAX_HISTORY:]

        # construir conversación
        messages = [system_prompt] + memory[user]

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.8,
            max_tokens=400
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
        return "🤖 Perdí el hilo… ¿puedes repetirlo?"