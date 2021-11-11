from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from pydantics.Application import AppOut
from services.ApplicationService import ApplicationService
from services.AuthService import AuthService
from services.TrackingService import TrackingService
from threading import Thread


app_router = APIRouter(tags=["App management"])


@app_router.get("/", response_model=List[AppOut])
async def get_app(user: dict = Depends(AuthService.get_current_user)):
    try:
        return ApplicationService.get_all_apps()
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app_router.delete("/{app_name}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_app(app_name: str, user: dict = Depends(AuthService.get_current_user)):
    try:
        ApplicationService.remove_app(app_name)
        # Tracking
        Thread(target=lambda: TrackingService.add_action(user["sub"], f"Remove app {app_name}")).start()
        # End tracking
        return
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
