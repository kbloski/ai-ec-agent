from fastapi import APIRouter
from application.handlers.test.test import test as test_handler

def register_test_routes(router: APIRouter):

    @router.get("/test")
    def test():
        return test_handler()