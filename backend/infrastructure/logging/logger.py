import logging
import os

class Logger:
    def __init__(self, name: str = "app-logger"):
        self._logger = logging.getLogger(name)

        # 👉 tworzenie folderu logs jeśli nie istnieje
        os.makedirs("logs", exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            handlers=[
                logging.FileHandler(f"logs/{name}.log", encoding="utf-8"),
                logging.StreamHandler()
            ]
        )

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)