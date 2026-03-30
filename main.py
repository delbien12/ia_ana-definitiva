from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

from brain import process

app = FastAPI()

# =============================
# INTERFAZ BONITA (/)
# =============================

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>A.N.A IA</title>

        <style>
            body {
                font-family: Arial;
                background: linear-gradient(135deg, #020617, #0f172a);
                color: white;
                margin: 0;
                text-align: center;
            }

            header {
                background: #020617;
                padding: 15px;
                font-size: 22px;
                color: #22d3ee;
                font-weight: bold;
            }

            button {
                margin: 10px;
                padding: 10px 15px;
                border: none;
                border-radius: 10px;
                background: #22d3ee;
                color: black;
                cursor: pointer;
                font-weight: bold;
            }

            #chatBox {
                display: none;
                max-width: 400px;
                margin: auto;
                background: #020617;
                height: 400px;
                overflow-y: auto;
                padding: 10px;
                border-radius: 15px;
                box-shadow: 0 0 15px #22d3ee55;
            }

            .msg {
                padding: 10px;
                margin: 6px;
                border-radius: 12px;
                max-width: 70%;
                word-wrap: break-word;
            }

            .user {
                background: #22d3ee;
                color: black;
                margin-left: auto;
                text-align: right;
            }

            .bot {
                background: #0ea5e9;
                text-align: left;
            }

            #inputArea {
                display: none;
                margin-top: 10px;
            }

            input {
                padding: 10px;
                width: 60%;
                border-radius: 8px;
                border: none;
                outline: none;
            }
        </style>
    </head>

    <body>

        <header>🤖 A.N.A IA</header>

        <div>
            <button onclick="abrirChat()">💬 Chat</button>
            <button onclick="window.location.href='/docs'">🧪 Pruebas</button>
        </div>

        <div id="chatBox"></div>

        <div id="inputArea">
            <input id="msg" placeholder="Escribe tu mensaje..." />
            <button onclick="enviar()">Enviar</button>
        </div>

        <script>
            function abrirChat() {
                document.getElementById("chatBox").style.display = "block";
                document.getElementById("inputArea").style.display = "block";
            }

            function agregarMensaje(texto, tipo) {
                let div = document.createElement("div");
                div.className = "msg " + tipo;
                div.innerText = texto;

                document.getElementById("chatBox").appendChild(div);
                document.getElementById("chatBox").scrollTop = 9999;
            }

            async function enviar() {
                let input = document.getElementById("msg");
                let mensaje = input.value;

                if (!mensaje) return;

                agregarMensaje(mensaje, "user");
                input.value = "";

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

                agregarMensaje(data.respuesta, "bot");
            }
        </script>

    </body>
    </html>
    """

# =============================
# MODELO
# =============================

class Chat(BaseModel):
    user: str
    message: str

# =============================
# API CHAT (NO TOCAR)
# =============================

@app.post("/chat")
def chat(data: Chat):
    respuesta = process(data.user, data.message)

    return {
        "status": "ok",
        "respuesta": respuesta
    }