import os
import json

def setup_cors():
    """Configura y procesa los orígenes CORS permitidos"""
    
    # Obtener y procesar los orígenes permitidos
    cors_env = os.getenv("CORS_ORIGINS", "")
    
    try:
        # Limpiar la cadena de caracteres escapados
        cors_env = cors_env.replace('\\"', '"')
        
        # Intentar parsear como JSON
        if cors_env.strip().startswith("["):
            CORS_ORIGINS = json.loads(cors_env)
        else:
            CORS_ORIGINS = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
            
        print(f"📝 CORS_ORIGINS cargados: {CORS_ORIGINS}")
        
    except json.JSONDecodeError as e:
        print(f"⚠️ Error parseando CORS_ORIGINS: {cors_env}")
        print(f"⚠️ Error detallado: {str(e)}")
        CORS_ORIGINS = [origin.strip() for origin in cors_env.split(",") if origin.strip()]

    if not CORS_ORIGINS:
        raise ValueError("⛔ CORS_ORIGINS debe estar definido en las variables de entorno")

    # Procesar orígenes
    processed_origins = []
    allow_origin_regex = None
    
    for origin in CORS_ORIGINS:
        if origin == "*":
            processed_origins = ["*"]
            break
        elif origin.startswith("*."):
            domain = origin.replace("*.", "").replace(".", r"\.")
            allow_origin_regex = rf"https://[^.]+\.{domain}"
        else:
            processed_origins.append(origin)

    print(f"🔒 Orígenes CORS permitidos: {processed_origins}")
    if allow_origin_regex:
        print(f"🔒 Patrón de subdominio permitido: {allow_origin_regex}")

    return processed_origins, allow_origin_regex 