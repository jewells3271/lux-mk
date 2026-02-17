import os
import sys

# Add the backend directory to sys.path so 'app' can be found
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
if backend_path not in sys.path:
    sys.path.append(backend_path)

try:
    from app.main import app
except Exception as e:
    # Fallback to a minimal app if the main one fails to boot (e.g., DB issues)
    import traceback
    error_msg = traceback.format_exc()
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI()
    
    # Add CORS to fallback app
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    async def catch_all(path_name: str):
        return JSONResponse(
            status_code=500,
            content={
                "status": "boot_error",
                "message": str(e),
                "traceback": error_msg.split('\n')
            }
        )

# Vercel requirements
app = app
