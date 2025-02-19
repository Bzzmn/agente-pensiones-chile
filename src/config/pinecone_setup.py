import os
from pinecone import Pinecone as PineconeClient
from langchain_pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

def setup_pinecone():
    """Configura y retorna el vector store de Pinecone"""
    try:
        # Initialize Pinecone client
        api_key = os.getenv("PINECONE_API_KEY")
        index_name = os.getenv("PINECONE_INDEX_NAME")
        
        print(f"🔑 Configurando Pinecone con índice: {index_name}")
        pc = PineconeClient(api_key=api_key)
        
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