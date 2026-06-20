from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware


class Routes:
    def __init__(self, app: FastAPI):
        self.app = app
        self.router = APIRouter()

        self.add_middleware()
        self.register()

    def add_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def register(self):
        @self.router.get("/health")
        def health():
            return {"status": "ok"}

        self.app.include_router(self.router)