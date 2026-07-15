from di.container import Container
from application.mappers.checklist_mapper import ChecklistMapper

def get_analyse_checklists_handler(analyse_id : int):
    container = Container()
    analyse_checklist_repository = container.analysis_checklist_repository()
    checklist_repository = container.checklist_repository()

    analyse_checklist_db = analyse_checklist_repository.find_by_analysis_id(analysis_id=analyse_id)
    checklists_ids = [ac.checklist_id for ac in analyse_checklist_db]

    checklists_db = checklist_repository.get_by_ids(ids=checklists_ids)
    checklists_dtos = [ ChecklistMapper.to_dto(item=ch) for ch in checklists_db]

    return checklists_dtos