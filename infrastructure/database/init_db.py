from .db import Base, engine
from . import models  # ważne: rejestracja modeli

def init_db():
    Base.metadata.create_all(bind=engine)