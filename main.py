from fastapi import FastAPI
from api.__routes__ import Routes
from di.container import Container
import uvicorn
from dotenv import load_dotenv
import infrastructure.database.init_db as init_db

load_dotenv()

# =========================
# FASTAPI APP
# =========================
app = FastAPI()
routes = Routes( app )
routes.register()

init_db.init_db()

if __name__ == "__main__":
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

