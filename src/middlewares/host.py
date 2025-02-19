from fastapi import Request
from fastapi.responses import JSONResponse
import os
import json

def get_allowed_hosts():
    """Obtiene los hosts permitidos desde CORS_ORIGINS"""
    cors_env = os.getenv("CORS_ORIGINS", "")
    try:
        if cors_env.strip().startswith("["):
            origins = json.loads(cors_env)
        else:
            origins = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
        
        # Convertir https:// URLs a hostnames
        hosts = [origin.replace("https://", "") for origin in origins if origin != "*"]
        return hosts
    except:
        return []

async def validate_host(request: Request, call_next):
    host = request.headers.get("host", "").split(":")[0]
    allowed_hosts = get_allowed_hosts()
    
    # Siempre permitir localhost para desarrollo
    if host in ["localhost", "127.0.0.1"]:
        return await call_next(request)
        
    # Si * está en CORS_ORIGINS, permitir cualquier host
    if "*" in os.getenv("CORS_ORIGINS", ""):
        return await call_next(request)
    
    if host not in allowed_hosts:
        return JSONResponse(
            status_code=403,
            content={
                "error": "Acceso denegado",
                "detail": "Host no permitido"
            }
        )
    return await call_next(request) 