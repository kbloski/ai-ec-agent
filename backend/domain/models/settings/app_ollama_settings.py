from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class AppOllamaSettings(Base, JSONSerializable):
    """Per-instance overrides for the Ollama connection/model settings that
    otherwise come from `.env` (`core/settings.py`). A single row (id=1),
    created lazily. Any nullable field left empty falls back to `.env`."""

    __tablename__ = TableName.APP_OLLAMA_SETTINGS.value

    id = Column(Integer, primary_key=True, autoincrement=True)

    ollama_url = Column(String, nullable=True)
    ollama_model = Column(String, nullable=True)
    ollama_timeout = Column(Integer, nullable=True)
    ollama_context_length = Column(Integer, nullable=True)
    ollama_temperature = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
