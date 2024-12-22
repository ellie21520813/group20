import aiofiles
import random
import string
import os

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from fastapi import FastAPI, File, UploadFile, Header
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Union
from pydantic import BaseModel

from app.db.session import get_db
from app.core.config import settings
from app.deps.auth import get_current_user_from_token
from app.schemas.file import FileCreate, FileShow
from app.schemas.pagination import Pagination, PaginationShow
from app.schemas.pagination_res import FilePaginationResponse
import app.db.repository.file as FileRepository


file_router = APIRouter()



# @file_router.post('/uploads', response_model=List[FileShow])
# async def upload_file(
#     files: List[UploadFile] = File(...), 
#     share: bool = False,
#     user: str = Depends(get_current_user_from_token),
#     db: Session = Depends(get_db)
# ):
#     response: List[FileShow]= []
#     for file in files:
#         file_name = file.filename
#         file_type = file.content_type
#         content   = await file.read()
#         file_size = len(content)
#         random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=settings.FILE_NAME_LENGTH))
#         ext = ""

#         if file_size > settings.MAX_SIZE_UPLOAD:
#             raise HTTPException(
#                 status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
#                 detail="File size is too big. Limit is 10mb"
#             )
            
#         if len(file_name.split(".")) > 1:
#             ext = f".{file_name.split('.')[-1]}"

#         new_name = f'{random_id}{ext}'
#         destination_file_path = f"/{settings.UPLOAD_FOLDER}/{new_name}"
#         async with aiofiles.open(destination_file_path, 'wb') as out_file:
#             await out_file.write(content)
        
#         file_create = FileCreate(
#             file_id=random_id,
#             is_public=bool(share),
#             local_url=destination_file_path,
#             name=file_name,
#             size=file_size,
#             type=file_type,
#             ext=ext,
#             # public_url=new_name,
#             created_by=user['username']
#         )
#         response.append(FileRepository.create_new_file(file_create, db))
#     return response


@file_router.post('/upload', response_model=FileShow)
async def upload_file(
    file: UploadFile = File(...), 
    share: bool = False,
    user: str = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
    authorization: Union[str, None] = Header(None)
):
    file_name = file.filename
    file_type = file.content_type
    content   = await file.read()
    file_size = len(content)
    token = authorization.replace("Bearer ", "")
    random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=settings.FILE_NAME_LENGTH))
    ext = ""

    if file_size > settings.MAX_SIZE_UPLOAD:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size is too big. Limit is 10mb"
        )
        
    if len(file_name.split(".")) > 1:
        ext = f".{file_name.split('.')[-1]}"

    new_name = f'{random_id}{ext}'
    destination_file_path = f"/{settings.UPLOAD_FOLDER}/{new_name}"
    async with aiofiles.open(destination_file_path, 'wb') as out_file:
        await out_file.write(content)
    
    file_create = FileCreate(
        file_id=random_id,
        is_public=bool(share),
        local_url=destination_file_path,
        name=file_name,
        size=file_size,
        type=file_type,
        ext=ext,
        created_by=user['username']
    )
    return FileRepository.create_new_file(file_create, token, db)


@file_router.delete('/{file_id}', response_model=FileShow)
async def delete_file(
    file_id: str,
    user = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    file: FileShow = FileRepository.get_file_by_id(file_id, db)
    if not user['is_superuser'] and file.created_by != user['username']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted!!!!"
        )
    file: FileShow = FileRepository.delete_file_by_id(file_id, db)
    try:
        if file:
            os.remove(file.local_url)
    except:
        pass
    return file


@file_router.post('/all', response_model=FilePaginationResponse)
async def get_all_files(
    pagination: Pagination,
    user: str = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    if user['is_superuser']:
        return FileRepository.get_all_file(pagination=pagination, db=db)
    return FileRepository.get_my_files_and_public(pagination=pagination, username=user['username'], db=db)


@file_router.post('/my-files', response_model=FilePaginationResponse)
async def get_my_files(
    user: str = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    return FileRepository.get_my_files(user['username'], db=db)


@file_router.get('/{file_id}/detail', response_model=FileShow)
async def get_file_detail(
    file_id: str,
    user: str = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
): 
    file: FileShow = FileRepository.get_file_by_id(file_id, db)
    if not file.is_public and file.created_by != user['username']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted!!!!"
        )
    
    return file


@file_router.get('/{file_id}', response_class=FileResponse)
def view_file(
    file_id: str,
    # user: str = Depends(get_current_user_from_token),
    token: str,
    db: Session = Depends(get_db)
): 
    file_id = file_id.split('.')[0]
    print(file_id)
    file: FileShow = FileRepository.get_file_by_id(file_id, db)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found!!!!"
        )
    user = get_current_user_from_token(token=token)
    if not user["is_superuser"] and not file.is_public and file.created_by != user['username']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted!!!!"
        )
    def iterfile():
        with open(file.local_url, 'rb') as f:
            yield from f
    return StreamingResponse(iterfile(), media_type=file.type)


@file_router.get('/{file_id}/download', response_class=FileResponse)
def download_file(
    file_id: str,
    # user: str = Depends(get_current_user_from_token),
    token: str,
    db: Session = Depends(get_db)
): 
    file_id = file_id.split('.')[0]
    file: FileShow = FileRepository.get_file_by_id(file_id, db)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found!!!!"
        )
    user = get_current_user_from_token(token=token)
    if not file.is_public and file.created_by != user['username']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted!!!!"
        )
    return FileResponse(
        path=file.local_url,
        filename=file.name
    )