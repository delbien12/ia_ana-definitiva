import re

def detect_medical(text):
    text = text.lower()

    palabras_medicas = [
        "dolor",
        "fiebre",
        "tos",
        "gripa",
        "gripe",
        "enfermo",
        "síntomas",
        "sintomas",
        "medicina",
        "medico",
        "doctor",
        "cabeza",
        "estómago",
        "estomago",
        "náusea",
        "nausea",
        "mareo",
        "vomito",
        "vomitar",
        "diarrea",
        "covid",
        "temperatura","dolor", "fiebre", "tos", "gripa", "enfermo", "síntomas", 
    "medicina", "médico", "doctor", "cabeza", "estomago",
    "curar", "remedio", "tratamiento", "aliviar","tomar", "pastilla" # <-- Agrega estas
        
    ]

    for palabra in palabras_medicas:
        if palabra in text:
            return True

    return False


def medical_response(text):
    text = text.lower()

    if "fiebre" in text:
        return "🤒 La fiebre puede indicar infección. Si supera 38°C consulta un médico."

    elif "cabeza" in text:
        return "🤕 El dolor de cabeza puede deberse a estrés, deshidratación o cansancio."

    elif "tos" in text:
        return "😷 La tos puede ser por resfriado o irritación. Si dura más de 3 días consulta médico."

    elif "estómago" in text or "estomago" in text:
        return "🤢 El dolor de estómago puede ser por comida o infección."

    elif "mareo" in text:
        return "😵 El mareo puede ser por presión baja o deshidratación."

    elif "cabeza" in text and ("curar" in text or "remedio" in text or "tratamiento" in text):
        return "🤕 Para el dolor de cabeza, se recomienda descansar en un lugar oscuro y hidratarse. Si persiste, consulta a un médico."

    elif "dolor de cabeza" in text:
        return "🤕 El dolor de cabeza puede deberse a estrés, deshidratación o falta de sueño."

    elif "fiebre" in text:
        return "🤒 La fiebre es una señal de que tu cuerpo lucha contra algo..."

    return "No estoy segura de cómo ayudarte con ese malestar específico, lo mejor es consultar a un profesional."
    return "⚕️ Podrías dar más detalles de los síntomas para ayudarte mejor."
