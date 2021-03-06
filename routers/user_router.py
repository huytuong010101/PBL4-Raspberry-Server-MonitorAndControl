from fastapi import APIRouter, HTTPException, status, Depends
from services.AuthService import AuthService
from typing import List
from pydantics.User import UserOut, UserIn, UserUpdate, Password
from services.UserSerivce import UserService
from services.TrackingService import TrackingService
from threading import Thread

user_router = APIRouter(tags=["User info"])


@user_router.get("", response_model=List[UserOut])
async def get_users(user: dict = Depends(AuthService.get_current_user)):
    try:
        return UserService.get_all()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@user_router.get("/profile", response_model=UserOut)
async def get_profile(user: dict = Depends(AuthService.get_current_user)):
    try:
        return UserService.get_by_id(user["sub"])
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@user_router.get("/{username}", response_model=UserOut)
async def get_user(username: str, user: dict = Depends(AuthService.get_current_user)):
    try:
        return UserService.get_by_id(username)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@user_router.put("/{username}/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
        username: str,
        password: Password,
        user: dict = Depends(AuthService.get_current_user)):
    if not user["is_admin"] and password.old_password is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    if not user["is_admin"] and username != user["sub"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    try:
        UserService.change_password(username, password.new_password, password.old_password)
        # Tracking
        Thread(target=lambda: TrackingService.add_action(user["sub"], "Change password of " + username)).start()
        # End tracking
        return
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@user_router.put("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def update(
        username: str,
        data: UserUpdate,
        user: dict = Depends(AuthService.get_current_user)):
    data = data.dict()
    if not user["is_admin"] and "is_admin" in data:
        del data["is_admin"]
    if not user["is_admin"] and username != data["username"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    try:
        UserService.update(username, data)
        # Tracking
        Thread(target=lambda: TrackingService.add_action(user["sub"], "Update " + username)).start()
        # End tracking
        return
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@user_router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def create(
        data: UserIn,
        user: dict = Depends(AuthService.get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    data = data.dict()
    data["created_by"] = user["sub"]
    try:
        UserService.create(data)
        # Tracking
        Thread(target=lambda: TrackingService.add_action(user["sub"], "Create user " + data.get("username"))).start()
        # End tracking
        return
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@user_router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        username: str,
        user: dict = Depends(AuthService.get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    try:
        UserService.delete(username)
        # Tracking
        Thread(target=lambda: TrackingService.add_action(user["sub"], "Delete user " + username)).start()
        # End tracking
        return
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )








