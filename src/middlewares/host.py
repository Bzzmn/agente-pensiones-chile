from fastapi import Request
from fastapi.responses import JSONResponse

async def validate_host(request: Request, call_next):
    host = request.headers.get("host", "").split(":")[0]
    allowed_hosts = request.app.state.allowed_hosts
    
    if host not in allowed_hosts and host not in ["localhost", "127.0.0.1"]:
        return JSONResponse(
            status_code=403,
            content={
                "error": "Acceso CORS denegado",
                "detail": "Host no permitido"
            }
        )
    return await call_next(request) 