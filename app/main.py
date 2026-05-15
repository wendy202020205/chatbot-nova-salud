from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para la pregunta
class Pregunta(BaseModel):
    query: str

# Endpoint raíz (para verificar que la API funciona)
@app.get("/")
def root():
    return {"mensaje": "API Nova Salud - Chatbot funcionando"}

# Endpoint POST /chat (el que usa tu frontend)
@app.post("/chat")
def chat(pregunta: Pregunta):
    # Respuesta de prueba para verificar la conexión
    return {"respuesta": f"Recibí tu pregunta: '{pregunta.query}'. La API funciona correctamente."}