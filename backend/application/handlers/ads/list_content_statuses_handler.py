from domain.enums.content_status import ContentStatus


def list_content_statuses_handler():
    return [{"value": status.value, "label": status.value.capitalize()} for status in ContentStatus]
