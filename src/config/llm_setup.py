import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Forzar recarga del .env
load_dotenv(override=True)

def setup_llm():
    """Configura y retorna el modelo de lenguaje"""
    try:
        print("🔄 Configurando modelo de lenguaje...")
        
        # Configurar LLM
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL"),
            temperature=0.2,
            base_url=os.getenv("OPENAI_BASE_URL"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        print(f"✅ Modelo LLM configurado: {llm.model_name}")
        return llm
        
    except Exception as e:
        print(f"❌ Error configurando LLM: {str(e)}")
        raise 