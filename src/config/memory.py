import os
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from dotenv import load_dotenv
import redis

# Cargar variables de entorno
load_dotenv()

def get_memory(session_id: str) -> ConversationBufferMemory:
    try:
        # Obtén la URL de conexión desde la variable de entorno
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        
        print(f"🔌 Conectando a Redis: {redis_url}")
        
        # Verificar conexión a Redis
        redis_client = redis.from_url(redis_url)
        redis_client.ping()  # Esto lanzará una excepción si no puede conectar
        
        # Crea una instancia de RedisChatMessageHistory con el ID de sesión
        chat_history = RedisChatMessageHistory(
            session_id=session_id,
            url=redis_url,
            key_prefix="chat:",  # Opcional: prefijo para las claves
            ttl=3600  # Opcional: tiempo de vida en segundos
        )
        
        # Crea la memoria del agente utilizando el historial almacenado en Redis
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            chat_memory=chat_history,
            return_messages=True
        )
        
        print("✅ Conexión a Redis establecida")
        return memory
        
    except redis.ConnectionError as e:
        print(f"❌ Error de conexión a Redis: {e}")
        print("⚠️ Usando memoria local como fallback")
        
        # Fallback a memoria local si Redis no está disponible
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        raise
