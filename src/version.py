import tomli
from pathlib import Path

def get_version_info():
    """Lee la información de versión desde pyproject.toml"""
    try:
        # Leer el archivo pyproject.toml
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            pyproject = tomli.load(f)
        
        return {
            "version": pyproject["project"]["version"],
            "name": "Agente de Pensiones",
            "description": pyproject["project"]["description"]
        }
    except Exception as e:
        print(f"⚠️ Error leyendo versión: {str(e)}")
        # Valores por defecto en caso de error
        return {
            "version": "0.0.0",
            "name": "Agente de Pensiones",
            "description": "Asistente virtual inteligente especializado en temas previsionales"
        } 