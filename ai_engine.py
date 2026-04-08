from groq import Groq
from config import GROQ_API_KEY, MODEL, TEMPERATURE, MAX_TOKENS

client = Groq(api_key=GROQ_API_KEY)

def generate(prompt):
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Eres A.N.A, una IA inteligente, útil, clara, amable, experta en matemáticas, salud básica, organización y apoyo emocional."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        return completion.choices[0].message.content

    except Exception as e:
        print("❌ Error Groq:", e)
        return "⚠️ Error con la IA en la nube."