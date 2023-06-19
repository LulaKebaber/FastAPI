from fastapi import Depends, Response

from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router


class CreateCommentRequest(AppModel):
    content: str


@router.post("/{shanyrak_id}/comments", response_model=CreateCommentRequest)
def create_comment(
    shanyrak_id: str,
    input: CreateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    comment = svc.repository.create_comment(shanyrak_id, jwt_data.user_id, input.dict())

    if comment is not None:
        return Response(status_code=200)
    else:
        return Response(status_code=404)
