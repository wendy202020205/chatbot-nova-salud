from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"mensaje": "API Nova Salud - Test básico funcionando"}

@app.post("/chat")
def chat(pregunta: dict):
    return {"respuesta": f"Pregunta recibida: {pregunta.get('query', '')}"}