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
ENV PORT=8001

# Exponer puerto
EXPOSE ${PORT}

# Validación de variables y ejecución
CMD ["sh", "-c", "\
    echo '🚀 Iniciando aplicación...' && \
    . /app/.venv/bin/activate && \
    uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"] 