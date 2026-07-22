from di.container import Container


def get_output_prompt_handler():

    container = Container()

    path_service = container.path_service()

    path = path_service.OUTPUT_RULES_PROMPT

    if not path.exists():
        return {"content": ""}

    return {"content": path.read_text(encoding="utf-8")}
