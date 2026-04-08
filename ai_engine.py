from groq import Groq
from config import GROQ_API_KEY, MODEL, TEMPERATURE, MAX_TOKENS

client = Groq(api_key=GROQ_API_KEY)

def get_prompt(modo):

    if modo == "medico":
        return "Eres un asistente médico. Das orientación general, nunca diagnóstico."

    if modo == "psicologo":
        return "Eres un psicólogo. Escucha, apoya emocionalmente y aconseja."

    if modo == "legal":
        return "Eres experto en leyes. Explicas derechos de forma clara."

    if modo == "organizador":
        return "Organiza tareas, horarios y planes paso a paso."

    return "Eres una IA inteligente que explica todo de forma clara."

def generate(messages, modo):
    try:
        system = {"role": "system", "content": get_prompt(modo)}

        completion = client.chat.completions.create(
            model=MODEL,
            messages=[system] + messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        return completion.choices[0].message.content

    except Exception as e:
        print("❌ Error IA:", e)
        return "⚠️ Error con la IA"