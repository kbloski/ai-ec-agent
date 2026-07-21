from di.container import Container


def delete_analysis_question_handler(id: int):
    container = Container()
    analysis_questions_repository = container.analysis_questions_repository()

    deleted = analysis_questions_repository.delete(id=id)

    return {"deleted": deleted}
