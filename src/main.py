from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from src.config.pinecone_setup import setup_pinecone
from src.config.memory import get_memory
from src.graph.agent import create_agent_graph
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv
from src.middlewares.cors import CORSMiddlewareWithErrorHandling
from src.middlewares.host import validate_host
from src.config.cors import setup_cors
from src.version import get_version_info
from src.config.llm_setup import setup_llm

# Cargar variables de entorno
load_dotenv()

# Obtener información de versión
version_info = get_version_info()

# Inicializar FastAPI con metadata
app = FastAPI(
    title="Agente de Pensiones API",
    description="API del Asistente Virtual de Pensiones",
    version=version_info["version"]
)

# Configurar logging con versión
print(f"\n🚀 Iniciando {version_info['name']} v{version_info['version']}")
print(f"📝 {version_info['description']}\n")

# Configurar CORS
processed_origins, allow_origin_regex = setup_cors()

# Configurar CORS con el middleware personalizado
app.add_middleware(
    CORSMiddlewareWithErrorHandling,
    allow_origins=processed_origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
    max_age=3600,
)

# Añadir middleware para hosts confiables
if "*" not in processed_origins:
    # Guardar hosts permitidos en el estado de la app
    app.state.allowed_hosts = [origin.replace("https://", "") for origin in processed_origins]
    app.middleware("http")(validate_host)

# Modelo para la solicitud
class EdadData(BaseModel):
    anos: int
    meses: int

class UserData(BaseModel):
    nombre: str
    genero: str
    edad: EdadData
    nivelEstudios: str

class ChatRequest(BaseModel):
    session_id: str
    user_message: str
    message_type: str
    agent_name: str
    user_data: UserData

# Inicializar componentes globales
print("\n🔧 Inicializando componentes...")

# Configurar el modelo de lenguaje
llm = setup_llm()

# Configurar el vector store
vectorstore = setup_pinecone()
retriever = vectorstore.as_retriever()

print("\n✨ Todos los componentes inicializados correctamente")
print("🚀 API lista para recibir peticiones\n")

@app.get("/")
async def read_root():
    return {"message": "Bienvenido al API del Asistente de Previsión Social"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Obtener o crear memoria para la sesión
        memory = get_memory(request.session_id)
        
        # Crear el grafo del agente para esta sesión
        agent = await create_agent_graph(retriever, llm, memory)
        
        # Crear el estado inicial con el mensaje del usuario y sus datos
        initial_state = {
            "messages": [HumanMessage(content=request.user_message)],
            "agent_name": request.agent_name,
            "user_data": {
                "nombre": request.user_data.nombre,
                "genero": request.user_data.genero,
                "edad": request.user_data.edad.dict(),
                "nivelEstudios": request.user_data.nivelEstudios
            }
        }
        
        # Ejecutar el agente
        result = await agent.ainvoke(initial_state)
        
        # Extraer la última respuesta
        if result and isinstance(result, dict) and "messages" in result:
            messages = result["messages"]
            if messages and isinstance(messages, list) and len(messages) > 0:
                last_message = messages[-1]
                if hasattr(last_message, "content"):
                    return {"response": last_message.content}
                else:
                    return {"response": str(last_message)}
        
        raise HTTPException(status_code=500, detail="No se pudo generar una respuesta válida")
            
    except Exception as e:
        print(f"Error en el chat: {str(e)}")
        print(f"Tipo de error: {type(e)}")
        print(f"Resultado recibido: {result if 'result' in locals() else 'No hay resultado'}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/version")
async def get_version():
    return version_info

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 