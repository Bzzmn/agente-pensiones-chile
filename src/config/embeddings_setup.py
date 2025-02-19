import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Forzar recarga del .env
load_dotenv(override=True)

def setup_embeddings():
    """Configura y retorna el modelo de embeddings"""
    try:
        print("🔄 Configurando modelo de embeddings...")
        
        # Configurar embeddings
        embeddings = OpenAIEmbeddings(
            model=os.getenv("OPENAI_EMBEDDING_MODEL"),
            base_url=os.getenv("OPENAI_EMBEDDING_BASE_URL"),
            api_key=os.getenv("OPENAI_EMBEDDING_API_KEY")
        )
        
        print(f"✅ Modelo de embeddings configurado: {embeddings.model}")
        return embeddings
        
    except Exception as e:
        print(f"❌ Error configurando embeddings: {str(e)}")
        raise 