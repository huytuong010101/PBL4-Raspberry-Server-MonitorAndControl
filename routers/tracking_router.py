from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from services.TrackingService import TrackingService
from services.AuthService import AuthService
from pydantics.LoginLog import LoginLogOut
from pydantics.Resource import ResourceOut
from pydantics.Action import ActionOut
from datetime import datetime


tracking_router = APIRouter(tags=["Tracking"])


@tracking_router.get("/login-logs", response_model=List[LoginLogOut])
async def get_login_logs(
        username: str = "",
        start_time: datetime = None,
        end_time: datetime = None,
        user: dict = Depends(AuthService.get_current_user),
):
    try:
        return TrackingService.get_login_logs(username, start_time, end_time)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@tracking_router.get("/resource-tracking", response_model=List[ResourceOut])
async def get_resource_tracking(
        start_time: datetime = None,
        end_time: datetime = None,
        user: dict = Depends(AuthService.get_current_user),
):
    try:
        return TrackingService.get_resource_tracking(start_time, end_time)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@tracking_router.get("/action-tracking", response_model=List[ActionOut])
async def get_action_tracking(
        start_time: datetime = None,
        end_time: datetime = None,
        user: dict = Depends(AuthService.get_current_user),
):
    try:
        return TrackingService.get_action_tracking(start_time, end_time)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
