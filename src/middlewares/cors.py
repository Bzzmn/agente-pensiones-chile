from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

class CORSMiddlewareWithErrorHandling(CORSMiddleware):
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await super().__call__(scope, receive, send)
        
        request = Request(scope, receive)
        origin = request.headers.get("origin")
        
        # Si no hay origen y no permitimos cualquier origen, bloqueamos
        if not origin and "*" not in self.allow_origins:
            response = JSONResponse(
                status_code=403,
                content={
                    "error": "Acceso CORS denegado",
                    "detail": "Origen no especificado o no permitido"
                }
            )
            return await response(scope, receive, send)
        
        # Si hay origen y no está permitido
        if origin and origin not in self.allow_origins and "*" not in self.allow_origins:
            response = JSONResponse(
                status_code=403,
                content={
                    "error": "Acceso CORS denegado",
                    "detail": "Origen no permitido"
                }
            )
            return await response(scope, receive, send)
            
        return await super().__call__(scope, receive, send) 