from fastapi import Depends, Response, UploadFile, HTTPException

from app.utils import AppModel

from typing import List, Any

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router


class UpdateShanyrakResponse(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str

class DeletePhotoRequest(AppModel):
    media: list


@router.patch("/{shanyrak_id:str}")
def update_shanyrak(
    shanyrak_id: str,
    input: UpdateShanyrakResponse,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak_updated = svc.repository.update_shanyrak(
        shanyrak_id, jwt_data.user_id, input.dict()
    )
    if shanyrak_updated.modified_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)


@router.post("/{shanyrak_id:str}/media")
def upload_shanyrak_photos(
    shanyrak_id: str,
    files: List[UploadFile],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Any:
    
    media_urls = []

    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename)
        media_urls.append(url)
    
    update_result = svc.repository.update_shanyrak(shanyrak_id, jwt_data.user_id, data={"media": media_urls})
    
    if update_result.acknowledged:
        return media_urls
    raise HTTPException(status_code=404, detail=f"Error occured while updating shanyrak {shanyrak_id}")

@router.delete("/{shanyrak_id:str}/media")
def delete_shanyrak_photos(
    shanyrak_id: str,
    input: DeletePhotoRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Any:
    
    shanyrak = svc.repository.get_shanyrak(shanyrak_id=shanyrak_id, user_id=jwt_data.user_id)
    media = shanyrak["media"]
    for file in input:
        svc.s3_service.delete_file(file.filename)
        del media[f"{file.filename}"]

    update_result = svc.repository.update_shanyrak(shanyrak_id, jwt_data.user_id, data={"media": media})
    if not update_result.acknowledged:
        raise HTTPException(status_code=404, detail=f"Error occured while deleting photos from shanyrak {shanyrak}")
    return Response(status_code=200)

    

        