.PHONY: install run test clean build-docker run-docker rebuild-docker stop-docker

# Variables
VENV = .venv
PORT = 8001
IMAGE_NAME = agente-pension
CONTAINER_NAME = agente-pension-container

# Crear entorno virtual e instalar dependencias
install:
	uv venv
	. $(VENV)/bin/activate && uv pip install -e .

# Ejecutar la aplicación en modo desarrollo
run:
	. $(VENV)/bin/activate && uvicorn src.main:app --reload --port $(PORT)

# Limpiar archivos temporales y cache
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete

# Limpiar imágenes Docker antiguas
clean-docker:
	@echo "🧹 Limpiando Docker completamente..."
	-docker stop $(CONTAINER_NAME) 2>/dev/null || true
	-docker rm $(CONTAINER_NAME) 2>/dev/null || true
	-docker rmi -f $$(docker images $(IMAGE_NAME) -q) 2>/dev/null || true
	-docker rmi -f $$(docker images -f "dangling=true" -q) 2>/dev/null || true
	-docker builder prune -f
	@echo "✨ Limpieza completada"

# Verificar contexto de construcción
check-context:
	@echo "🔍 Verificando archivos de configuración..."
	@echo "📂 src/config:"
	@ls -la src/config

# Construir imagen Docker
build-docker: clean-docker check-context
	@echo "🔨 Construyendo nueva imagen..."
	docker build --no-cache --quiet -t $(IMAGE_NAME) .
	@echo "✅ Imagen construida exitosamente"

# Detener contenedor Docker si está corriendo
stop-docker:
	@echo "🛑 Deteniendo contenedor..."
	-docker stop $(CONTAINER_NAME) 2>/dev/null || true
	-docker rm $(CONTAINER_NAME) 2>/dev/null || true
	@echo "✅ Contenedor detenido"

# Ejecutar contenedor Docker localmente
run-docker: stop-docker
	docker run --name $(CONTAINER_NAME) -p $(PORT):80 --env-file .env $(IMAGE_NAME)

run-dev-docker:
	docker run --name $(CONTAINER_NAME) -p $(PORT):$(PORT) --env-file .env $(IMAGE_NAME)

# Reconstruir y ejecutar Docker
rebuild-docker: build-docker run-dev-docker

# Ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make install       - Crear entorno virtual e instalar dependencias"
	@echo "  make run          - Ejecutar aplicación en modo desarrollo"
	@echo "  make clean        - Limpiar archivos temporales y cache"
	@echo "  make clean-docker - Limpiar imágenes Docker antiguas"
	@echo "  make build-docker - Construir imagen Docker (limpia imágenes antiguas)"
	@echo "  make stop-docker  - Detener contenedor Docker si está corriendo"
	@echo "  make run-docker   - Ejecutar contenedor Docker localmente"
	@echo "  make rebuild-docker- Reconstruir y ejecutar Docker" 