from di.container import Container


def delete_analysis_handler(id: int):
    container = Container()
    analysis_repository = container.analysis_repository()
    analysis_questions_repository = container.analysis_questions_repository()
    knowledge_analysis_repository = container.knowledge_analysis_repository()

    analysis_questions = analysis_questions_repository.find_for_analyse(analysis_id=id)
    for analysis_question in analysis_questions:
        analysis_questions_repository.delete(id=analysis_question.id)

    knowledge_analysis_repository.delete_by_analysis_id(analysis_id=id)

    deleted = analysis_repository.delete(id=id)

    return {"deleted": deleted}
