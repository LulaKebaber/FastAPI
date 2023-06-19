from typing import Any

from fastapi import Depends, Response
from pydantic import Field


from app.utils import AppModel

from ..service import Service, get_service

from . import router


class GetCommentResponse(AppModel):
    id: Any = Field(alias="_id")
    content: str
    created_at: str
    author_id: str


@router.get("/{shanyrak_id:str}/comments", response_model=GetCommentResponse)
def get_shanyrak(
    shanyrak_id: str,
    svc: Service = Depends(get_service),
) -> list:
    comments = svc.repository.get_comments(shanyrak_id)
    if comments is None:
        return Response(status_code=404)
    return GetCommentResponse(**comments)
