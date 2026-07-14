from domain.models.checklist.checklist_item import ChecklistItem
from application.dtos.checklist.checklist_item_dto import ChecklistItemDto

class ChecklistItemMapper:

    @staticmethod
    def to_dto(item : ChecklistItem) -> ChecklistItemDto:
        return ChecklistItemDto(
            id = item.id,
            checklist_id= item.checklist_id,
            question=item.question,
            answer=item.answer,
            notes=item.notes
        )

