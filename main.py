from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import ollama
import time
import logging
from api.routes import Routes
from di.container import Container
import uvicorn

# =========================
# FASTAPI APP
# =========================
app = FastAPI()
routes = Routes( app )
routes.register()

if __name__ == "__main__":

    # =========================
    # DI
    # =========================
    container = Container()
    logger = container.logger()
    logger.info("Application started successfully")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )

