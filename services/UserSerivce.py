from models.User import User
from typing import List
from fastapi import HTTPException, status
from utils.auth import AuthUtil


class UserService:
    @staticmethod
    def get_all() -> List[User]:
        return list(User.select())

    @staticmethod
    def get_by_id(username: str):
        user = User.get_or_none(username=username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    @staticmethod
    def change_password(username: str, new_password: str, old_password: str = None):
        user = User.get_or_none(username=username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if old_password and not AuthUtil.verify_password(old_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Old password is wrong"
            )
        user.password = AuthUtil.get_password_hash(new_password)
        user.save()

    @staticmethod
    def update(username, data):
        user = User.get_or_none(username=username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if data.get("username"):
            del data["username"]
        if data.get("password"):
            del data["password"]
        User.update(**data).where(User.username == username).execute()

    @staticmethod
    def create(data: dict):
        user = User.get_or_none(username=data["username"])
        if user is not None:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Username is already used")
        data["password"] = AuthUtil.get_password_hash(data["password"])
        User.create(**data)


