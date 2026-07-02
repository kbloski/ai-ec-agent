from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import ollama
import time
import logging
from api.__routes__ import Routes
from di.container import Container
import uvicorn
from dotenv import load_dotenv
import os 
import infrastructure.database.init_db as init_db

load_dotenv()

# =========================
# FASTAPI APP
# =========================
app = FastAPI()
routes = Routes( app )
routes.register()

if __name__ == "__main__":
    init_db.init_db()

    # =========================
    # DI
    # =========================
    container = Container()
    settings = container.settings()
    logger = container.logger()

    host = settings.get_host()
    port = settings.get_port()
    model = settings.get_ollama_llm_model()


    logger.info(f"Application started successfully url=http://{host}:{port}")
    logger.info(f"Using Ollama model: {model}")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    )

