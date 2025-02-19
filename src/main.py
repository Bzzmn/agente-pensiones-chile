from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
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

# Cargar variables de entorno
load_dotenv()

# Inicializar FastAPI
app = FastAPI()

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
class ChatRequest(BaseModel):
    session_id: str
    user_message: str
    message_type: str
    agent_name: str

# Inicializar componentes globales
print("\n🔧 Inicializando componentes...")

# Configurar el modelo de lenguaje
llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL"),
        temperature=0.2,
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY")
)

print(f"Modelo LLM: {llm.model_name}")

# Configurar el vector store
vectorstore = setup_pinecone()
retriever = vectorstore.as_retriever(
    # search_type="similarity",
    # search_kwargs={"k": 3}
)

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
        
        # Crear el estado inicial con el mensaje del usuario
        initial_state = {
            "messages": [HumanMessage(content=request.user_message)],
            "agent_name": request.agent_name  # Pasamos el nombre del agente en el estado
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 