from fastapi import Depends, Response

from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router


class UpdateCommentResponse(AppModel):
    content: str


@router.patch("/{shanyrak_id:str}/comments/{comment_id:str}")
def update_comment(
    shanyrak_id: str,
    comment_id: str,
    input: UpdateCommentResponse,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    comment_updated = svc.repository.update_comment(comment_id, jwt_data.user_id, input)

    if comment_updated.modified_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)


@router.delete("/{shanyrak_id:str}/comments/{comment_id:str}")
def delete_shanyrak(
    shanyrak_id: str,
    comment_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    shanyrak_deleted = svc.repository.delete_comment(comment_id, jwt_data.user_id)
    if shanyrak_deleted.deleted_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)
