import os

from jose import ExpiredSignatureError, JWTError

from pydantics.File import FileOut
from fastapi import HTTPException, status, UploadFile
from fastapi.responses import FileResponse
import shutil
from utils.auth import AuthUtil
from datetime import timedelta


class FileService:
    @staticmethod
    def get_all_file(base_path: str):
        if not os.path.isdir(base_path):
            raise HTTPException(status_code=404, detail="Đường dẫn không tồn tại")
        res = []
        for file_name in os.listdir(base_path):
            full_path = os.path.join(base_path, file_name)
            file = FileOut(
                name=file_name,
                size=os.path.getsize(full_path) if os.path.isfile(full_path) else None,
                type="file" if os.path.isfile(full_path) else "dir",
                modified_at=os.path.getmtime(full_path),
                created_at=os.path.getctime(full_path),
            )
            res.append(file)

        return res

    @staticmethod
    def rename(file_path: str, name: str):
        dir_path = os.path.dirname(file_path)
        new_file_path = os.path.join(dir_path, name)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tệp tin")
        if os.path.exists(new_file_path):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Tên đã tồn tại")
        os.rename(file_path, new_file_path)

    @staticmethod
    def delete(file_path: str):
        if not os.path.exists(file_path):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tệp tin")
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            shutil.rmtree(file_path, ignore_errors=True)

    @staticmethod
    def create_dir(base_path: str, dir_name: str):
        full_path = os.path.join(base_path, dir_name)
        if os.path.exists(full_path):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Tên này đã tồn tại")
        os.mkdir(full_path)

    @staticmethod
    async def upload_file(base_path: str, file: UploadFile):
        file_name = file.filename
        full_path = os.path.join(base_path, file_name)
        while os.path.exists(full_path):
            file_name = "_" + file_name
            full_path = os.path.join(base_path, file_name)
        content = await file.read()
        with open(full_path, "wb") as f:
            f.write(content)

    @staticmethod
    async def create_download_token(path):
        data = {
            "path": path
        }
        return AuthUtil.create_access_token(data, timedelta(minutes=2))

    @staticmethod
    async def response_file(token: str):
        try:
            data = AuthUtil.decode_token(token)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not os.path.isfile(data.get("path")):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tệp tin")
        return FileResponse(data.get("path"))
