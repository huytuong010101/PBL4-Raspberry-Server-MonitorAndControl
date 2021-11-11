from fastapi import APIRouter, HTTPException, status, File, UploadFile, Depends
from pydantics.File import FileOut, FileUpdate, DirIn
from typing import List
from services.FileService import FileService
from services.AuthService import AuthService
from services.TrackingService import TrackingService
from threading import Thread


file_router = APIRouter(tags=["File management"])


@file_router.get("/", response_model=List[FileOut])
async def get_file(base_path: str = "/", user: dict = Depends(AuthService.get_current_user)):
    try:
        return FileService.get_all_file(base_path)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@file_router.get("/download/{file_path:path}", status_code=status.HTTP_200_OK)
async def get_file(file_path: str, user: dict = Depends(AuthService.get_current_user)):
    try:
        return await FileService.create_download_token(file_path)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@file_router.get("/stream-file/{token}", status_code=status.HTTP_200_OK)
async def response_file(token: str):
    try:
        return await FileService.response_file(token)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@file_router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def rename(data: FileUpdate, user: dict = Depends(AuthService.get_current_user)):
    try:
        FileService.rename(data.path, data.name)
        # Tracking
        Thread(target=lambda: TrackingService.add_action(user["sub"], f"Rename {data.path} to {data.name}")).start()
        # End tracking
        return
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@file_router.delete("/{file_path:path}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(file_path: str, user: dict = Depends(AuthService.get_current_user)):
    try:
        FileService.delete(file_path)
        # Tracking
        Thread(target=lambda: TrackingService.add_action(user["sub"], f"Delete file {file_path}")).start()
        # End tracking
        return
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@file_router.post("/dir", status_code=status.HTTP_204_NO_CONTENT)
async def create_dir(data: DirIn, user: dict = Depends(AuthService.get_current_user)):
    try:
        FileService.create_dir(data.base_path, data.dir_name)
        # Tracking
        Thread(target=
               lambda: TrackingService.add_action(user["sub"], f"Create folder {data.dir_name} in {data.base_path}")
               ).start()
        # End tracking
        return
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@file_router.post("/upload_file", status_code=status.HTTP_204_NO_CONTENT)
async def upload_file(base_path: str, file: UploadFile = File(...), user: dict = Depends(AuthService.get_current_user)):
    try:
        await FileService.upload_file(base_path, file)
        # Tracking
        Thread(target=lambda: TrackingService.add_action(user["sub"], f"Upload {file.filename} to {base_path}")).start()
        # End tracking
        return
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
