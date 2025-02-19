import os
from pinecone import Pinecone as PineconeClient
from langchain_pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Forzar recarga del .env
load_dotenv(override=True)

def setup_pinecone():
    """Configura y retorna el vector store de Pinecone"""
    try:
        # Debug de variables de entorno
        print("\n🔍 Debug variables Pinecone:")
        print(f"ENV FILE API KEY: {os.getenv('PINECONE_API_KEY')}")
        print(f"ENV FILE ENV: {os.getenv('PINECONE_ENV')}")
        print(f"ENV FILE INDEX: {os.getenv('PINECONE_INDEX_NAME')}")
        
        # Al inicio de la función
        print("\n🔍 Todas las variables de entorno con 'PINECONE':")
        for key in os.environ:
            if 'PINECONE' in key:
                print(f"{key}: {os.environ[key][:10]}...")
        
        # Initialize Pinecone client
        api_key = os.getenv("PINECONE_API_KEY", "").strip()  # Asegurar que no hay espacios
        index_name = os.getenv("PINECONE_INDEX_NAME")
        
        if not api_key:
            raise ValueError("❌ PINECONE_API_KEY no encontrada en variables de entorno")
            
        if not api_key.startswith("pcsk_"):
            raise ValueError(f"❌ PINECONE_API_KEY inválida o mal formateada (debe empezar con 'pcsk_'). Valor actual: {api_key[:10]}...")
            
        print(f"🔑 Configurando Pinecone con índice: {index_name}")
        
        # Intentar inicializar el cliente primero
        pc = PineconeClient(api_key=api_key)
        
        # Verificar conexión listando índices
        try:
            pc.list_indexes()
            print("✅ Conexión a Pinecone verificada")
        except Exception as e:
            print(f"❌ Error conectando a Pinecone: {str(e)}")
            raise
        
        # Setup embeddings
        embedding = OpenAIEmbeddings(
            model=os.getenv("OPENAI_EMBEDDING_MODEL"),
            base_url=os.getenv("OPENAI_EMBEDDING_BASE_URL"),
            api_key=os.getenv("OPENAI_EMBEDDING_API_KEY")
        )
        print(f"✅ Embeddings configurados: {embedding.model}")
        
        # Create vector store
        vectorstore = Pinecone.from_existing_index(
            index_name=index_name,
            embedding=embedding
        )
        print("✅ Vector store configurado exitosamente")
        return vectorstore
        
    except Exception as e:
        print(f"❌ Error configurando Pinecone: {str(e)}")
        print(f"🔍 Tipo de error: {type(e)}")
        raise 