import os
import json

def setup_cors():
    """Configura y procesa los orígenes CORS permitidos"""
    
    # Obtener y procesar los orígenes permitidos
    cors_env = os.getenv("CORS_ORIGINS", "")
    try:
        # Intentar parsear como JSON si comienza con [
        if cors_env.strip().startswith("["):
            CORS_ORIGINS = json.loads(cors_env)
        else:
            CORS_ORIGINS = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
    except json.JSONDecodeError:
        CORS_ORIGINS = [origin.strip() for origin in cors_env.split(",") if origin.strip()]

    if not CORS_ORIGINS:
        raise ValueError("⛔ CORS_ORIGINS debe estar definido en las variables de entorno")

    # Verificar si se permite cualquier origen
    if "*" in CORS_ORIGINS:
        print("⚠️ Advertencia: CORS configurado para permitir cualquier origen")
        processed_origins = ["*"]
        allow_origin_regex = None
    else:
        # Procesar orígenes para manejar comodines
        processed_origins = []
        allow_origin_regex = None
        
        for origin in CORS_ORIGINS:
            if origin.startswith("*."):
                # Convertir *.domain.com a regex pattern
                domain = origin.replace("*.", "").replace(".", "\.")
                allow_origin_regex = rf"https://[^.]+\.{domain}"
            else:
                processed_origins.append(origin)

    print(f"🔒 Orígenes CORS permitidos: {processed_origins}")
    if allow_origin_regex:
        print(f"🔒 Patrón de subdominio permitido: {allow_origin_regex}")

    return processed_origins, allow_origin_regex 