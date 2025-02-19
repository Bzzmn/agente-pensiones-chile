FROM python:3.12-slim

WORKDIR /app

# Instalar uv
RUN pip install uv

# Copiar solo los archivos necesarios
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Instalar dependencias usando uv con --system
RUN uv pip install --system -e .

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
ENV PORT=8001

# Exponer puerto
EXPOSE ${PORT}

# Validación de variables requeridas al inicio
CMD ["sh", "-c", "[ -n \"$OPENAI_API_KEY\" ] && [ -n \"$OPENAI_EMBEDDING_API_KEY\" ] && [ -n \"$PINECONE_API_KEY\" ] && [ -n \"$REDIS_URL\" ] && uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"] 