from typing import Any

from fastapi import Depends
from fastapi import Field

from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


class CreateShanyraqRequest(AppModel):
    type: str
    price: int
    address: str
    area: int
    rooms_count: int
    description: str


class CreateShanyraqResponse(AppModel):
    id: Field(alias="_id")


@router.post("/", response_model=CreateShanyraqResponse)
def create_shanyrak(
    input: CreateShanyraqRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak_id = svc.repository.create_shanyrak(jwt_data.user_id, input.dict())

    return CreateShanyraqResponse(id=shanyrak_id)
