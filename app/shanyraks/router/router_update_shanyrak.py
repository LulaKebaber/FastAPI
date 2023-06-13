from typing import Any

from fastapi import Depends, Response
from pydantic import Field


from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router


class UpdateShanyraqResponse(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.patch("/{shanyrak_id:str}")
def get_shanyrak(
    shanyrak_id: str,
    input: UpdateShanyraqResponse,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak = svc.repository.update_shanyrak(shanyrak_id, input.dict())
    if shanyrak is None:
        return Response(status_code=404)
    return UpdateShanyraqResponse(**shanyrak)
