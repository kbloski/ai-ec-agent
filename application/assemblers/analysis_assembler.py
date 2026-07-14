from infrastructure.logging.logger import Logger
from application.dtos.analysis.analysis_dto import AnalysisDto
from application.dtos.analysis.analysis_question_dto import AnalysisQuestionDto
from application.mappers.analysis_question_mapper import AnalysisQuestionMapper
from infrastructure.repositories.analysis_questions_repository import AnalysisQuestionsRepository

class AnalysisAssembler:
    logger : Logger
    analysis_questions_repository : AnalysisQuestionsRepository

    def __init__(
        self,
        logger : Logger,
        analysis_questions_repository : AnalysisQuestionsRepository
    ):
        self.logger = logger
        self.analysis_questions_repository = analysis_questions_repository

    def assemble_dto(self, item : AnalysisDto) -> AnalysisDto:
        
        analysis_questins_db = self.analysis_questions_repository.find_for_analyse(analysis_id=item.id)
        analysis_questions_dtos = [AnalysisQuestionMapper.to_dto(aq) for aq in analysis_questins_db]
        item.anlysis_questions = analysis_questions_dtos

        return item
    

