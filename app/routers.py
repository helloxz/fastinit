from fastapi import APIRouter
from app.api.index import IndexHandler

index_handler = IndexHandler()

router = APIRouter()

router.get("/")(index_handler.index)