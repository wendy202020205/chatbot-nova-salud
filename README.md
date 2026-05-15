# Chatbot Nova Salud - Farmacia

Chatbot RAG con LangChain, Gemini y FAISS para consultas de productos y horarios.

## Tecnologías
- LangChain (orquestación RAG)
- Google Gemini 2.5 Flash (modelo IA)
- FAISS (búsqueda semántica)
- FastAPI + Docker (backend en Render)
- React (frontend)

## Arquitectura
Usuario → Web (React) → API (Render) → LangChain → FAISS → Gemini → Respuesta

## URLs
- API: https://chatbot-nova-salud.onrender.com
- Repositorio: https://github.com/wendy202020205/chatbot-nova-salud

## Ejemplos de preguntas
- ¿Cuánto cuesta la aspirina?
- Horario de atención domingos
- ¿Tienen delivery gratis?

## Autor
Wendy - Proyecto para curso de Ingeniería de Software con IA