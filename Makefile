.PHONY: install run test clean build-docker run-docker

# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python
UV = $(VENV)/bin/uv
PORT = 8001

# Crear entorno virtual e instalar dependencias
install:
	python -m venv $(VENV)
	pip install uv
	$(UV) pip install -e .

# Ejecutar la aplicación en modo desarrollo
run:
	$(PYTHON) -m uvicorn src.main:app --reload --port $(PORT)

# Limpiar archivos temporales y cache
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete

# Construir imagen Docker
build-docker:
	docker build -t agente-pension .

# Ejecutar contenedor Docker localmente
run-docker:
	docker run -p $(PORT):$(PORT) --env-file .env agente-pension

# Ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make install      - Crear entorno virtual e instalar dependencias"
	@echo "  make run         - Ejecutar aplicación en modo desarrollo"
	@echo "  make clean       - Limpiar archivos temporales y cache"
	@echo "  make build-docker- Construir imagen Docker"
	@echo "  make run-docker  - Ejecutar contenedor Docker localmente" 