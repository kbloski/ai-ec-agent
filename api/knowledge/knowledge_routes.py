from fastapi import APIRouter
from di.container import Container

def register_knowledge_routes(router: APIRouter):

    @router.get("/knowledge/build")
    def knowledge_build():

        container = Container()

        knowledge_service = container.knowledge_service()

        knowledge_service.build_knowledge_from_materials_raw()

        return {
            "status": "ok",
            "knowledge_build": True
        }