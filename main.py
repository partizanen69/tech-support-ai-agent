import logging
from src.db.db import execute_raw_sql, get_session
from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
from src.chat.chat_routes import router as chat_router
logger = logging.getLogger("uvicorn.error")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
  
@app.get("/healthcheck")
async def health_check():
    try:
        await execute_raw_sql("SELECT 1")
        return {"status": "ok"}
    except Exception as e:
        logger.exception(f"Health check failed: {e}")
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"status": "error", "detail": str(e)})

@app.get("/")
def serve_frontend():
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend.html")
    return FileResponse(frontend_path) 
