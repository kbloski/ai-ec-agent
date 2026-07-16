from di.container import Container

def knowledge_advertisement_generate_handler(knowledge_id : int ):
    container = Container()
    
    knowledge_service = container.knowledge_service()
    
    knowledge_details = knowledge_service.get_knowledge_details_by_id(knowledge_id=knowledge_id)
    
    return "Knowledge advetisement generate"