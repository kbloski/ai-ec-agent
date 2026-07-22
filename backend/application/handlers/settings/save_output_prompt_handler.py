from di.container import Container


def save_output_prompt_handler(content: str):

    container = Container()

    path_service = container.path_service()

    path = path_service.OUTPUT_RULES_PROMPT

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    return {"content": content}
