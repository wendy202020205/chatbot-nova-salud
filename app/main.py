from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
import os

app = FastAPI()

# Configurar CORS para que tu web pueda llamar a esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pregunta(BaseModel):
    query: str

# Cargar API key desde variable de entorno (la configurarás en Render)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

print("🔄 Cargando documento...")
loader = TextLoader("data/nova_salud_farmacia.txt", encoding="utf-8")
documentos = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documentos)

print("🔄 Creando embeddings...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = Chroma.from_documents(chunks, embeddings)

print("🔄 Configurando modelo...")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=False
)
print("✅ API lista")

@app.get("/")
def root():
    return {"mensaje": "API Nova Salud - Chatbot funcionando"}

@app.post("/chat")
def chat(pregunta: Pregunta):
    respuesta = qa_chain.invoke({"query": pregunta.query})
    return {"respuesta": respuesta["result"]}