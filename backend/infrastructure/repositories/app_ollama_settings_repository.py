from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from domain.models.settings.app_ollama_settings import AppOllamaSettings
from infrastructure.logging.logger import Logger

SETTINGS_ROW_ID = 1


class AppOllamaSettingsRepository:
    def __init__(self, logger: Logger, db: Session):
        self.db = db

    def get(self) -> Optional[AppOllamaSettings]:
        return self.db.query(AppOllamaSettings).filter(AppOllamaSettings.id == SETTINGS_ROW_ID).first()

    def upsert(self, fields: Dict[str, Any]) -> AppOllamaSettings:
        item = self.get()

        if item is None:
            item = AppOllamaSettings(id=SETTINGS_ROW_ID)
            self.db.add(item)

        for key, value in fields.items():
            setattr(item, key, value)

        self.db.commit()
        self.db.refresh(item)

        return item
