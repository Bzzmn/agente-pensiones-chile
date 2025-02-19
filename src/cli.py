from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from graph.agent import create_agent_graph, AgentState
from langchain_core.messages import HumanMessage, AIMessage
from src.config.pinecone_setup import setup_pinecone
import uuid
from src.config.memory import get_memory
import os

async def main():
    # Cargar variables de entorno
    load_dotenv()
    
    print("\n🔧 Inicializando sistema...")
    
    # Configurar Pinecone y LLM
    pinecone_index = setup_pinecone()
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL"),
        temperature=0.2,
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY")
        )
    
    print("Modelo LLM: ", llm.model_name)
    
    # Generar un session_id único
    session_id = str(uuid.uuid4())
    print(f"🔑 Session ID: {session_id}")
    
    # Configurar la memoria con Redis
    print("📦 Configurando memoria...")
    memory = get_memory(session_id)
    
    # Inicializar el grafo
    print("🔄 Inicializando grafo de conversación...")
    graph = await create_agent_graph(
        retriever=pinecone_index.as_retriever(),
        llm=llm,
        memory=memory
    )
    
    print("\n✨ ¡Bienvenido al Asistente Previsional! ✨")
    print("Escribe 'salir' para terminar")
    print("Escribe 'memoria' para ver el historial de la conversación\n")
    
    while True:
        pregunta = input("👤 Tu pregunta: ")
        
        if pregunta.lower() in ['salir', 'exit', 'quit']:
            print("\n👋 ¡Hasta luego!")
            break
            
        if pregunta.lower() == 'memoria':
            print("\n💭 Historial de conversación:")
            print(memory.load_memory_variables({})["chat_history"])
            continue
            
        try:
            print("\n🔄 Procesando tu pregunta...")
            
            initial_state: AgentState = {
                "messages": [HumanMessage(content=pregunta)],
                "context": None,
                "chat_history": memory.load_memory_variables({}).get("chat_history", ""),
                "next_step": None,
                "time_info": None,
                "sources": None,
                "agent_name": "Alexandra"  # Nombre por defecto para el CLI
            }
            
            async for output in graph.astream(initial_state):
                for key, value in output.items():
                    if value["messages"] and isinstance(value["messages"][-1], AIMessage):
                        print(f"\n🤖 {value['messages'][-1].content}")
            
            print("\n" + "-"*50 + "\n")
                
        except Exception as e:
            print("\n❌ Error:", str(e))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())