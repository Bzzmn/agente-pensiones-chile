import os
from pinecone import Pinecone as PineconeClient
from langchain_pinecone import Pinecone
from src.config.embeddings_setup import setup_embeddings
from dotenv import load_dotenv

# Forzar recarga del .env
load_dotenv(override=True)

def setup_pinecone():
    """Configura y retorna el vector store de Pinecone"""
    try:
        # Initialize Pinecone client
        api_key = os.getenv("PINECONE_API_KEY", "").strip()
        index_name = os.getenv("PINECONE_INDEX_NAME")
        
        if not api_key:
            raise ValueError("❌ PINECONE_API_KEY no encontrada en variables de entorno")
            
        if not api_key.startswith("pcsk_"):
            raise ValueError("❌ PINECONE_API_KEY inválida o mal formateada (debe empezar con 'pcsk_')")
            
        print(f"🔄 Configurando conexión a Pinecone...")
        
        # Intentar inicializar el cliente
        pc = PineconeClient(api_key=api_key)
        
        # Verificar conexión
        pc.list_indexes()
        
        # Setup embeddings
        embedding = setup_embeddings()
        
        # Create vector store
        vectorstore = Pinecone.from_existing_index(
            index_name=index_name,
            embedding=embedding
        )
        print("✅ Conexión a Pinecone establecida")
        return vectorstore
        
    except Exception as e:
        print(f"❌ Error configurando Pinecone: {str(e)}")
        raise 