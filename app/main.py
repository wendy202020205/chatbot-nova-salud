from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pregunta(BaseModel):
    query: str

# Configurar Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('models/gemini-pro-latest')
else:
    print("⚠️ ADVERTENCIA: GOOGLE_API_KEY no configurada")

# Cargar el documento de Nova Salud
try:
    with open("data/nova_salud_farmacia.txt", "r", encoding="utf-8") as f:
        documento = f.read()
    print("✅ Documento cargado correctamente")
except FileNotFoundError:
    print("❌ ERROR: No se encontró el archivo data/nova_salud_farmacia.txt")
    documento = ""

@app.get("/")
def root():
    return {"mensaje": "API Nova Salud - Chatbot funcionando"}

@app.post("/chat")
def chat(pregunta: Pregunta):
    # Si no hay API key o documento, responder con mensaje de error
    if not GOOGLE_API_KEY:
        return {"respuesta": "Error: API key de Gemini no configurada en Render"}
    
    if not documento:
        return {"respuesta": "Error: Documento de Nova Salud no encontrado"}
    
    # Construir el prompt
    prompt = f"""Eres un asistente de atención al cliente de NOVA SALUD, una farmacia.
Responde SOLO basándote en la siguiente información de la farmacia.
Si la pregunta no tiene respuesta en el documento, di: "No tengo esa información en mis documentos".

INFORMACIÓN DE NOVA SALUD:
{documento}

PREGUNTA DEL CLIENTE: {pregunta.query}

RESPUESTA (sé amable y conciso):"""
    
    try:
        respuesta = model.generate_content(prompt)
        return {"respuesta": respuesta.text}
    except Exception as e:
        return {"respuesta": f"Error al generar respuesta: {str(e)}"}
