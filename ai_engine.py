from groq import Groq
from config import GROQ_API_KEY, MODEL, TEMPERATURE, MAX_TOKENS

client = Groq(api_key=GROQ_API_KEY)

def generate(messages, tipo="normal"):
    
    # 🎯 CONTROL DINÁMICO
    if tipo == "matematicas":
        max_tokens = 60
    elif tipo == "codigo":
        max_tokens = 300
    else:
        max_tokens = MAX_TOKENS
    try:
        completion = client.chat.completions.create(
            messages=messages,
            model=MODEL,
            temperature=TEMPERATURE,
            max_tokens=max_tokens
        )

        return completion.choices[0].message.content

    except Exception as e:
        print("❌ Error Groq:", e)
        return "⚠️ Error con la IA en la nube."
