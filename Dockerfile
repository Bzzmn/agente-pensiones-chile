FROM python:3.12-slim

WORKDIR /app

# Instalar uv globalmente
RUN pip install --no-cache-dir uv

# Copiar solo los archivos necesarios
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Instalar dependencias usando uv
RUN uv venv /app/.venv && \
    . /app/.venv/bin/activate && \
    uv pip install -e .

# Variables requeridas (documentación)
ENV OPENAI_API_KEY=""
ENV OPENAI_MODEL=""
ENV OPENAI_BASE_URL=""
ENV OPENAI_EMBEDDING_MODEL=""
ENV OPENAI_EMBEDDING_BASE_URL=""
ENV OPENAI_EMBEDDING_API_KEY=""
ENV REDIS_URL=""
ENV PINECONE_API_KEY=""
ENV PINECONE_ENV=""
ENV PINECONE_INDEX_NAME=""
ENV CORS_ORIGINS=""
ENV PORT=80 
# Exponer puerto
EXPOSE ${PORT}

# Validación de variables requeridas al inicio y ejecución usando el venv
CMD ["sh", "-c", "\
    echo 'Verificando variables de entorno...' && \
    echo 'Puerto configurado:' && echo $PORT && \
    echo 'PINECONE_API_KEY=' && echo $PINECONE_API_KEY | cut -c1-10 && \
    echo 'PINECONE_ENV=' && echo $PINECONE_ENV && \
    echo 'PINECONE_INDEX_NAME=' && echo $PINECONE_INDEX_NAME && \
    [ -n \"$OPENAI_API_KEY\" ] && \
    [ -n \"$OPENAI_EMBEDDING_API_KEY\" ] && \
    [ -n \"$PINECONE_API_KEY\" ] && \
    [ -n \"$REDIS_URL\" ] && \
    . /app/.venv/bin/activate && \
    uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"] 