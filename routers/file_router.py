from fastapi import APIRouter, HTTPException, status, File, UploadFile
from pydantics.File import FileOut, FileUpdate, DirIn
from typing import List
from services.FileService import FileService


file_router = APIRouter(tags=["File management"])


@file_router.get("/", response_model=List[FileOut])
async def get_file(base_path: str = "/"):
    try:
        return FileService.get_all_file(base_path)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@file_router.get("/download/{file_path:path}", status_code=status.HTTP_200_OK)
async def get_file(file_path: str):
    try:
        return FileService.get_file(file_path)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@file_router.put("/{file_path:path}", status_code=status.HTTP_204_NO_CONTENT)
async def rename(file_path: str, data: FileUpdate):
    try:
        FileService.rename(file_path, data.name)
        return
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@file_router.delete("/{file_path:path}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(file_path: str):
    try:
        FileService.delete(file_path)
        return
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@file_router.post("/dir", status_code=status.HTTP_204_NO_CONTENT)
async def create_dir(data: DirIn):
    try:
        FileService.create_dir(data.base_path, data.dir_name)
        return
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@file_router.post("/upload_file", status_code=status.HTTP_204_NO_CONTENT)
async def upload_file(base_path: str, file: UploadFile = File(...)):
    try:
        await FileService.upload_file(base_path, file)
        return
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
