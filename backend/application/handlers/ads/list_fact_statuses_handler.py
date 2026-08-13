from domain.enums.fact_status import FactStatus


def list_fact_statuses_handler():
    return [{"value": status.value, "label": status.value.capitalize()} for status in FactStatus]
