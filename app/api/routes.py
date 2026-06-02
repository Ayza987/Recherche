from fastapi import APIRouter

from app.services.master_service import MasterService
from app.config import MASTER_1_IP

router = APIRouter()


@router.get("/tree")
async def get_tree():

    master = MasterService(MASTER_1_IP)

    return await master.request(
        1,
        "/gettree"
    )