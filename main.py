from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from brain import process

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user: str
    message: str

# 🌐 INTERFAZ EN /chat
@app.get("/chat", response_class=HTMLResponse)
def chat_ui():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{margin:0;font-family:Arial;background:#020617;color:white;display:flex;flex-direction:column;height:100vh;}
header{text-align:center;padding:10px;color:#22d3ee;box-shadow:0 0 10px #22d3ee;}
#chat{flex:1;overflow:auto;padding:10px;display:flex;flex-direction:column;}
.msg{padding:10px;margin:5px;border-radius:10px;max-width:80%;}
.user{background:#22d3ee;color:black;align-self:flex-end;}
.bot{background:#0ea5e9;align-self:flex-start;}
#inputArea{display:flex;padding:10px;border-top:1px solid #22d3ee;}
input{flex:1;padding:10px;border-radius:10px;border:none;}
button{padding:10px;margin-left:5px;background:#22d3ee;border:none;border-radius:10px;}
</style>
</head>

<body>

<header>🤖 A.N.A IA</header>

<div id="chat"></div>

<div id="inputArea">
<input id="msg" placeholder="Escribe..." />
<button onclick="send()">➤</button>
</div>

<script>
const chat = document.getElementById("chat");
const input = document.getElementById("msg");

input.addEventListener("keypress", e=>{
 if(e.key==="Enter") send();
});

function add(text,type){
 let d=document.createElement("div");
 d.className="msg "+type;
 d.innerText=text;
 chat.appendChild(d);
 chat.scrollTop=9999;
}

async function send(){
 let m=input.value;
 if(!m) return;

 add(m,"user");
 input.value="";

 let r=await fetch("/chat",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({user:"web",message:m})
 });

 let data=await r.json();

 add(data.respuesta,"bot");
}
</script>

</body>
</html>
"""

# 🧠 API (Mendix)
@app.post("/chat")
def chat(req: ChatRequest):
    return {"status": "ok", "respuesta": process(req.user, req.message)}