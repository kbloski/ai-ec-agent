from domain.enums.review_status import ReviewStatus


def list_review_statuses_handler():
    return [{"value": status.value, "label": status.value.capitalize()} for status in ReviewStatus]
