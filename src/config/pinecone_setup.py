import os
from pinecone import Pinecone as PineconeClient
from langchain_pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

def setup_pinecone():
    # Initialize Pinecone client
    pc = PineconeClient(api_key=os.getenv("PINECONE_API_KEY"))
    
    # Setup embeddings
    embedding = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL"),
        base_url=os.getenv("OPENAI_EMBEDDING_BASE_URL"),
        api_key=os.getenv("OPENAI_EMBEDDING_API_KEY")
    )
    print(f"Usando modelo de embeddings: {embedding.model}") 
    
    # Create vector store
    return Pinecone.from_existing_index(
        index_name=os.getenv("PINECONE_INDEX_NAME"),
        embedding=embedding
    ) 