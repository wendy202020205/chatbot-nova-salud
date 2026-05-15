from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pregunta(BaseModel):
    query: str

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Esta es la parte que cambiamos ---
print("🔄 Cargando documento/s...")
documentos = []
docs_path = "data/"

# Cargar el archivo TXT
txt_path = os.path.join(docs_path, "nova_salud_farmacia.txt")
if os.path.exists(txt_path):
    loader_txt = TextLoader(txt_path, encoding="utf-8")
    documentos.extend(loader_txt.load())
    print("✅ Documento TXT cargado correctamente.")
else:
    print("❌ No se encontró el archivo TXT en la carpeta data/")

# Cargar el archivo PDF
pdf_path = os.path.join(docs_path, "nova_salud_farmacia.pdf")
if os.path.exists(pdf_path):
    loader_pdf = PyPDFLoader(pdf_path)
    documentos.extend(loader_pdf.load())
    print("✅ Documento PDF cargado correctamente.")
else:
    print("❌ No se encontró el archivo PDF en la carpeta data/")
# --- Fin de la modificación ---

# Verificamos si se cargó al menos un documento
if not documentos:
    raise Exception("No se pudo cargar ningún documento (TXT o PDF). Revisa la carpeta data/")

# El resto del código sigue igual
print(f"Total de páginas/fragmentos cargados: {len(documentos)}")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documentos)

print("🔄 Creando embeddings con FAISS...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = FAISS.from_documents(chunks, embeddings)

print("🔄 Configurando modelo...")
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0.5)
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
