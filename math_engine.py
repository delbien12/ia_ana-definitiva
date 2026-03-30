import sympy as sp
import re

x = sp.symbols('x')

def preprocess(text):
    text = text.lower()

    # limpiar frases humanas
    text = re.sub(
        r"(cu[aá]nto es|cual es|cu[aá]l es|calcula|resuelve|puedes decirme)",
        "",
        text
    )

    text = text.replace("?", "")

    # 🔥 eliminar basura BIEN
    text = re.sub(r"\b(la|el|de|y)\b", " ", text)

    # raíces
    text = re.sub(r"ra[ií]z cuadrada\s*(\d+)", r"sqrt(\1)", text)
    text = re.sub(r"ra[ií]z\s*(\d+)", r"sqrt(\1)", text)

    # potencias
    text = re.sub(r"(\d+)\s*al cuadrado", r"\1**2", text)

    # operaciones
    reglas = {
        "más": "+",
        "mas": "+",
        "menos": "-",
        "por": "*",
        "entre": "/",
        "dividido entre": "/"
    }

    for k, v in reglas.items():
        text = text.replace(k, v)

    # limpiar espacios
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def solve(text):
    try:
        clean = preprocess(text)
        print("DEBUG:", clean)  # 👈 para ver qué está procesando

        expr = sp.sympify(clean, evaluate=True)

        if "=" in clean:
            left, right = clean.split("=")
            eq = sp.Eq(sp.sympify(left), sp.sympify(right))
            sol = sp.solve(eq, x)
            return f"📘 Solución: {sol}"

        return f"🧮 Resultado: {sp.N(expr)}"

    except Exception as e:
        print("❌ Error matemático:", e)
        return None