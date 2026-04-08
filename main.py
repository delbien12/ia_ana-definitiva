from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from brain import process

app = FastAPI()

# 🔓 Permitir conexión (Mendix / web / celular)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📩 Modelo de datos
class ChatRequest(BaseModel):
    user: str
    message: str


# 🌐 INTERFAZ WEB (CHAT NEÓN)
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>A.N.A IA</title>

<style>
body {
    margin: 0;
    font-family: Arial;
    background: #020617;
    color: white;
    display: flex;
    flex-direction: column;
    height: 100vh;
}

header {
    padding: 15px;
    text-align: center;
    color: #22d3ee;
    font-weight: bold;
    font-size: 20px;
    box-shadow: 0 0 10px #22d3ee;
}

#chat {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
    display: flex;
    flex-direction: column;
}

.msg {
    padding: 10px;
    margin: 5px;
    border-radius: 12px;
    max-width: 75%;
    word-wrap: break-word;
    animation: fadeIn 0.3s ease;
}

.user {
    background: #22d3ee;
    color: black;
    align-self: flex-end;
}

.bot {
    background: #0ea5e9;
    align-self: flex-start;
    box-shadow: 0 0 10px #22d3ee55;
}

.typing {
    font-style: italic;
    opacity: 0.7;
}

#inputArea {
    display: flex;
    padding: 10px;
    border-top: 1px solid #22d3ee;
}

input {
    flex: 1;
    padding: 10px;
    border-radius: 10px;
    border: none;
    outline: none;
}

button {
    margin-left: 5px;
    padding: 10px;
    border-radius: 10px;
    border: none;
    background: #22d3ee;
    cursor: pointer;
    font-weight: bold;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(5px);}
    to {opacity: 1;}
}

@media (max-width: 600px) {
    .msg {
        max-width: 90%;
    }
}
</style>
</head>

<body>

<header>
🤖 A.N.A IA
<button onclick="limpiarChat()">🧹</button>
</header>

<div id="chat"></div>

<div id="inputArea">
    <input id="msg" placeholder="Escribe tu mensaje..." />
    <button onclick="enviar()">➤</button>
</div>

<script>
const chat = document.getElementById("chat");
const input = document.getElementById("msg");

/* Cargar historial */
window.onload = () => {
    let saved = localStorage.getItem("chat");
    if (saved) {
        chat.innerHTML = saved;
        chat.scrollTop = chat.scrollHeight;
    }
};

/* Guardar historial */
function guardar() {
    localStorage.setItem("chat", chat.innerHTML);
}

/* ENTER */
input.addEventListener("keypress", function(e) {
    if (e.key === "Enter") enviar();
});

/* Mensajes */
function agregarMensaje(texto, tipo) {
    let div = document.createElement("div");
    div.className = "msg " + tipo;
    div.innerText = texto;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    guardar();
}

/* Typing */
let typingDiv = null;

function mostrarTyping() {
    typingDiv = document.createElement("div");
    typingDiv.className = "msg bot typing";
    typingDiv.innerText = "Escribiendo...";
    chat.appendChild(typingDiv);
    chat.scrollTop = chat.scrollHeight;
}

function quitarTyping() {
    if (typingDiv) {
        chat.removeChild(typingDiv);
        typingDiv = null;
    }
}

/* Enviar */
async function enviar() {
    let mensaje = input.value.trim();
    if (!mensaje) return;

    agregarMensaje(mensaje, "user");
    input.value = "";

    mostrarTyping();

    try {
        let res = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user: "web",
                message: mensaje
            })
        });

        let data = await res.json();

        quitarTyping();
        agregarMensaje(data.respuesta, "bot");

    } catch (err) {
        quitarTyping();
        agregarMensaje("⚠️ Error con la IA", "bot");
    }
}

/* Limpiar chat */
function limpiarChat() {
    chat.innerHTML = "";
    localStorage.removeItem("chat");
}
</script>

</body>
</html>
"""


# 🧠 API CHAT
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        respuesta = process(req.user, req.message)

        if not respuesta:
            return {
                "status": "ok",
                "respuesta": "🤖 No pude procesar eso, intenta diferente."
            }

        return {
            "status": "ok",
            "respuesta": respuesta
        }

    except Exception as e:
        print("❌ Error general:", e)
        return {
            "status": "error",
            "respuesta": "⚠️ Error interno del servidor."
        }