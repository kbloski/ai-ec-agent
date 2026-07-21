from di.container import Container
from application.mappers.analysis_mapper import AnalysisMapper

def get_analysis_by_id_handler(analyse_id : int):
    container = Container()

    analysis_repository = container.analysis_repository()
    analysis_assembler = container.analysis_assembler()


    analysis_db = analysis_repository.get_by_id(id=analyse_id)
    dto = AnalysisMapper.to_dto(analysis_db)
    assembled = analysis_assembler.assemble_dto(dto)

    return assembled