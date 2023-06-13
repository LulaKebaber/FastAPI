from fastapi import Depends, Response

from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router


@router.patch("/{shanyrak_id:str}")
def delete_shanyrak(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak_deleted = svc.repository.delete_shanyrak(shanyrak_id, jwt_data.user_id)
    if shanyrak_deleted.modified_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)
