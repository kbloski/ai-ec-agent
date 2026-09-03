from typing import Optional

from fastapi import HTTPException
from ollama import Client

from di.container import Container


def list_ollama_models_handler(url: Optional[str] = None):
    container = Container()
    settings = container.settings()
    repository = container.app_ollama_settings_repository()

    if url:
        host = url
    else:
        overrides = repository.get()
        host = (overrides.ollama_url if overrides else None) or settings.get_ollama_url()

    try:
        client = Client(host=host)
        response = client.list()
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Nie udało się połączyć z Ollama pod adresem {host}: {e}",
        )

    return {
        "models": [model.model for model in response.models if model.model],
    }
