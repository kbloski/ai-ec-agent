from di.container import Container
from application.mappers.checklist_mapper import ChecklistMapper

def get_checklist_by_id_handler(checklist_id : int):
    container = Container()
    checklist_repostiory = container.checklist_repository()
    checklist_assembler = container.checklist_assembler()

    checklist_db = checklist_repostiory.get_by_id(id=checklist_id)
    checklist_dto = ChecklistMapper.to_dto(item=checklist_db)
    assembled_checklist = checklist_assembler.assemble_dto(item=checklist_dto)

    return assembled_checklist