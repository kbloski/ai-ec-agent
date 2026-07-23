from infrastructure.logging.logger import Logger
from application.dtos.analysis.analysis_dto import AnalysisDto
from application.mappers.analysis_question_mapper import AnalysisQuestionMapper
from infrastructure.repositories.analysis_questions_repository import AnalysisQuestionsRepository
from infrastructure.repositories.question_answer_repository import QuestionAnswerRepository

class AnalysisAssembler:
    logger : Logger
    analysis_questions_repository : AnalysisQuestionsRepository
    question_answer_repository : QuestionAnswerRepository

    def __init__(
        self,
        logger : Logger,
        analysis_questions_repository : AnalysisQuestionsRepository,
        question_answer_repository : QuestionAnswerRepository
    ):
        self.logger = logger
        self.analysis_questions_repository = analysis_questions_repository
        self.question_answer_repository = question_answer_repository

    def assemble_dto(self, item : AnalysisDto) -> AnalysisDto:

        analysis_questions_db = self.analysis_questions_repository.find_for_analyse(analysis_id=item.id)

        question_answer_ids = [aq.question_answer_id for aq in analysis_questions_db]
        question_answers_db = self.question_answer_repository.get_by_ids(ids=question_answer_ids)
        question_answers_by_id = {qa.id: qa for qa in question_answers_db}

        analysis_questions_dtos = [
            AnalysisQuestionMapper.to_dto(aq, question_answers_by_id[aq.question_answer_id])
            for aq in analysis_questions_db
            if aq.question_answer_id in question_answers_by_id
        ]
        item.analysis_questions = analysis_questions_dtos

        return item
