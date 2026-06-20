from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import ollama
import logging
import time

from api.routes import Routes

# =========================
# LOGGING SETUP
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ai-app")

# =========================
# FASTAPI APP
# =========================

app = FastAPI()

routes = Routes( app );
routes.register();

messages = []


# @app.get("/", response_class=HTMLResponse)
# def home():
#     logger.info("GET / (frontend loaded)")

#     with open("index.html", "r", encoding="utf-8") as f:
#         return f.read()


# # 📦 lista modeli z Ollamy
# @app.get("/models")
# def models():
#     logger.info("GET /models")

#     res = ollama.list()
#     model_list = [m["model"] for m in res["models"]]

#     logger.info(f"Available models: {model_list}")

#     return {"models": model_list}


# @app.post("/chat")
# def chat(data: dict):
#     global messages

#     start_time = time.time()

#     model = data["model"]
#     user_message = data["message"]

#     logger.info(f"User message: {user_message}")
#     logger.info(f"Selected model: {model}")

#     messages.append({"role": "user", "content": user_message})

#     try:
#         response = ollama.chat(
#             model=model,
#             messages=messages
#         )

#         reply = response["message"]["content"]

#         messages.append({"role": "assistant", "content": reply})

#         duration = round(time.time() - start_time, 3)

#         logger.info(f"AI response: {reply}")
#         logger.info(f"Response time: {duration}s")

#         return {"response": reply}

#     except Exception as e:
#         logger.error(f"Ollama error: {str(e)}")
#         return {"response": "Błąd AI"}