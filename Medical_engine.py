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
        "temperatura"
    ]

    for palabra in palabras_medicas:
        if palabra in text:
            return True

    return False


def medical_response(text):
    text = text.lower()

    if "fiebre" in text:
        return "🤒 La fiebre puede indicar infección. Si supera 38°C consulta un médico."

    elif "dolor de cabeza" in text:
        return "🤕 El dolor de cabeza puede deberse a estrés, deshidratación o cansancio."

    elif "tos" in text:
        return "😷 La tos puede ser por resfriado o irritación. Si dura más de 3 días consulta médico."

    elif "estómago" in text or "estomago" in text:
        return "🤢 El dolor de estómago puede ser por comida o infección."

    elif "mareo" in text:
        return "😵 El mareo puede ser por presión baja o deshidratación."

    return "⚕️ Podrías dar más detalles de los síntomas para ayudarte mejor."
