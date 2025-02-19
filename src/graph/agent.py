from typing import TypedDict, Annotated, Sequence, Dict, Any, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, Graph
from langchain_openai import ChatOpenAI
from langchain_core.retrievers import BaseRetriever
from datetime import datetime
import pytz

class TimeInfo(TypedDict):
    current_time: str
    timezone: str
    formatted_date: str

class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    context: str | None
    chat_history: str | None
    next_step: Literal["retrieve", "respond"] | None
    time_info: TimeInfo | None
    sources: list[str] | None
    agent_name: str | None

def get_formatted_time() -> TimeInfo:
    """Obtiene la información de tiempo formateada"""
    chile_tz = pytz.timezone('America/Santiago')
    now = datetime.now(chile_tz)
    
    return {
        "current_time": now.strftime("%H:%M:%S"),
        "timezone": "America/Santiago",
        "formatted_date": now.strftime("%Y-%m-%d")
    }

def print_state(state: Dict[str, Any]) -> None:
    """Imprime el estado actual del grafo de manera formateada"""
    print("\n" + "="*50)
    print("🔄 Estado actual del grafo:")
    
    # Imprimir mensajes
    if "messages" in state:
        print("\n📝 Mensajes:")
        for msg in state["messages"]:
            role = "👤 Usuario" if isinstance(msg, HumanMessage) else "🤖 Asistente"
            print(f"{role}: {msg.content}")
    
    # Imprimir contexto si existe
    if "context" in state and state["context"]:
        print("\n📚 Contexto recuperado:")
        print(state["context"][:200] + "..." if len(state["context"]) > 200 else state["context"])
    
    # Imprimir historial si existe
    if "chat_history" in state and state["chat_history"]:
        print("\n💭 Historial de chat:")
        print(state["chat_history"][:200] + "..." if len(state["chat_history"]) > 200 else state["chat_history"])
    
    print("="*50 + "\n")

def evaluate_need_for_context(state: AgentState) -> AgentState:
    """Evalúa si es necesario buscar información adicional dependiendo del contenido de la consulta."""
    query = state["messages"][-1].content.lower()

    # Palabras clave relacionadas con temas previsionales y pensiones
    pension_keywords = [
        # Palabras base
        "pensión", "pensiones", "previsional", "previsión", "previsión social",
        "reforma", "jubilación", "jubilacion", "jubilado", "pensionado", "fondo autonomo","bono",
        # Ahorro y aportes
        "ahorro previsional", "ahorro obligatorio", "aportes previsionales voluntarios", "aporte", 
        "cotización obligatoria", "cotizaciones voluntarias", "cotizaciones", "apv",
        
        # Entidades y siglas
        "afp", "afps", "administradora de fondos de pensiones", "fapp",
        "ips", "instituto de previsión social",
        "sp", "superintendencia de pensiones", 
        # Modelos y tipos de pensión
        "capitalización individual", "modelo de reparto", "retiro de fondos", "renta vitalicia",
        "retiro programado", "pilar solidario", "pilar contributivo", "pilar no contributivo",
        
        # Situaciones y beneficios
        "expectativa de vida", "pensión básica solidaria", "pensión de vejez", 
        "pensión de invalidez", "pensión de sobrevivencia", 
        "compensacion", "beneficios previsionales", "dictamen de pensiones",
        
        # Otros términos relevantes
        "edad de jubilación", "edad legal de jubilación", "jubilación anticipada", 
        "trabajador", "empleador", "cotizante", "certificado de cotizaciones", 
        "vejez"
    ]

    if any(phrase in query for phrase in pension_keywords):
        state["next_step"] = "retrieve"
    else:
        state["next_step"] = "respond"
        
    return state

def create_retrieval_chain(retriever: BaseRetriever):
    def retrieve_context(state: AgentState) -> AgentState:
        """Busca información relevante en Pinecone basada en el último mensaje"""
        print("\n🔍 Buscando información relevante...")
        query = state["messages"][-1].content
        
        # Buscar en Pinecone
        print("🔎 Consultando base de conocimiento...")
        docs = retriever.get_relevant_documents(query)
        
        # Formatear el contexto con metadatos relevantes y referencias numeradas
        formatted_docs = []
        sources = []
        
        for i, doc in enumerate(docs, 1):
            # Crear entrada formateada con metadatos y referencia
            formatted_entry = f"""
                [link_{i}]
                Título: {doc.metadata.get('title', 'Sin título')}
                Fecha de publicación: {doc.metadata.get('estimated_published_time', 'Fecha no especificada')}
                Fuente: {doc.metadata.get('source_domain', 'Dominio no especificado')}
                Contenido:
                {doc.page_content}
            """
            formatted_docs.append(formatted_entry)
            
            # Crear entrada de fuente con enlace HTML
            url = doc.metadata.get('url_source', '#')
            source = f'<a href="{url}" target="_blank">link_{i}</a>'
            sources.append(source)
        
        # Guardar en el estado
        state["context"] = "\n\n".join(formatted_docs)
        # Unir las fuentes con comas si hay más de una
        state["sources"] = ", ".join(sources) if len(sources) > 1 else sources[0] if sources else ""
        
        print(f"✅ Encontrados {len(docs)} documentos relevantes")
        return state
    return retrieve_context

def create_response_chain(llm: ChatOpenAI):
    context_template = """Eres {agent_name}, una asistente virtual con expertiz en temas previsionales.
    
    Información temporal actual:
    - Fecha: {date}
    - Hora: {time}
    - Zona horaria: {timezone}
    
    Contexto relevante:
    {context}
    
    Historial de la conversación:
    {chat_history}
    
    Pregunta actual: {question}
    
    Referencias disponibles:
    {sources}

    Instrucciones especiales:
        - No debes inventar información, solo debes usar el contexto y las referencias.
        - No debes realizar calculos financieros, solo debes dar una explicacion general.
        - Si el usuario te pide un calculo de pension indica que puede ocupar la calculadora de pesiones y presionando recalcular puede volver a calcular.
    
    Instrucciones de formato y estilo:
        1. Extensión
        - Máximo 250 palabras
        - Oraciones cortas y directas

        2. Estructura
        - Introducción breve (2-3 líneas)
        - 1 a 3 subtítulos con "##"
        - Puntos clave con "-"
        - Conclusión breve (opcional)

        3. Formato
        - **Negrita** para conceptos clave
        - *Cursiva* para términos importantes
        - > para una cita (máx. 1)
        - Una línea en blanco entre secciones

        4. Fuentes
        - Una línea en blanco antes de "Fuentes:"
        - Lista solo las fuentes realmente usadas
    
    Ejemplo de respuesta ideal:
    
        Introducción breve que presenta el tema principal.

        ## Aspectos Clave

        - **Primer punto**: explicación concisa  
        - **Segundo punto**: explicación concisa  
        - **Tercer punto**: explicación concisa  

        > Cita relevante (si es necesaria)

        Fuentes:
        {sources}
    """
    
    simple_template = """Eres un asistente experto en temas previsionales.
    Tu genero esta determinado por tu nombre {agent_name}.
    
    Información temporal actual:
    - Fecha: {date}
    - Hora: {time}
    - Zona horaria: {timezone}
    
    Historial de la conversación:
    {chat_history}

    Instrucciones especiales:
    - No debes responder preguntas que no estén relacionadas con los temas previsionales.
    - No puedes realizar asesoria financiera especifica, si el usuario te lo solicita, da consejos generales relacionados con el tema previsional.
    - No debes realizar calculos financieros, solo debes dar una explicacion general.
    - Si el usuario te pide un calculo de pension indica que puede ocupar nuestra calculadora de pesiones disponible en la pagina principal, presionando recalcular puede volver a ingrear los datos. No debes dar mas explicaciones.
    
    Responde de manera cordial y concisa al siguiente mensaje: {question}
    """
    
    def generate_response(state: AgentState) -> AgentState:
        """Genera una respuesta basada en el contexto y la pregunta"""
        print("\n🤔 Generando respuesta...")
        
        question = state["messages"][-1].content
        chat_history = state.get("chat_history", "No hay historial previo.")
        
        # Obtener información temporal actual
        time_info = get_formatted_time()
        
        # Si hay contexto y fuentes
        if state.get("context") and state.get("sources"):
            response = llm.invoke(context_template.format(
                agent_name=state.get("agent_name"),
                date=time_info["formatted_date"],
                time=time_info["current_time"],
                timezone=time_info["timezone"],
                context=state["context"],
                chat_history=chat_history,
                question=question,
                sources=state["sources"]
            ))
            
            # Asegurarnos de que la respuesta tenga el formato correcto de fuentes
            if "Fuentes:" not in response.content:
                response_content = response.content.strip() + f"\n\nFuentes:\n{state['sources']}"
                response = AIMessage(content=response_content)
        # Si no hay contexto, usar el template simple
        else:
            response = llm.invoke(simple_template.format(
                agent_name=state.get("agent_name"),
                date=time_info["formatted_date"],
                time=time_info["current_time"],
                timezone=time_info["timezone"],
                chat_history=chat_history,
                question=question
            ))
            response = AIMessage(content=response.content)
        
        print("✅ Respuesta generada")
        state["messages"].append(response)
        return state
    
    return generate_response

def remember_interaction(state: AgentState, memory) -> AgentState:
    """Guarda la interacción en la memoria y actualiza el contexto conversacional"""
    print("\n💾 Guardando interacción en memoria...")
    
    if len(state["messages"]) >= 2:
        memory.save_context(
            {"input": state["messages"][-2].content},
            {"output": state["messages"][-1].content}
        )
        chat_history = memory.load_memory_variables({})["chat_history"]
        state["chat_history"] = chat_history
        print("✅ Memoria actualizada")
    return state

async def create_agent_graph(retriever: BaseRetriever, llm: ChatOpenAI, memory) -> Graph:
    workflow = StateGraph(AgentState)
    
    # Agregar nodos
    workflow.add_node("evaluate", evaluate_need_for_context)
    workflow.add_node("retrieve", create_retrieval_chain(retriever))
    workflow.add_node("respond", create_response_chain(llm))
    workflow.add_node("remember", lambda state: remember_interaction(state, memory))
    
    # Definir el flujo
    workflow.set_entry_point("evaluate")
    
    # Agregar edges condicionales
    workflow.add_conditional_edges(
        "evaluate",
        lambda x: x["next_step"],
        {
            "retrieve": "retrieve",
            "respond": "respond"
        }
    )
    
    # Continuar el flujo
    workflow.add_edge("retrieve", "respond")
    workflow.add_edge("respond", "remember")
    
    # Compilar el grafo
    return workflow.compile(debug=True) 