from di.container import Container


def delete_checklist_item_handler(id: int):
    container = Container()
    checklist_items_repository = container.checklist_items_repository()

    deleted = checklist_items_repository.delete(id=id)

    return {"deleted": deleted}
