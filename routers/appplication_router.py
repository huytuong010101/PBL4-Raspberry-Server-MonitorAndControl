from fastapi import APIRouter, HTTPException, status
from typing import List
from pydantics.Application import AppOut
from services.ApplicationService import ApplicationService


app_router = APIRouter(tags=["App management"])


@app_router.get("/", response_model=List[AppOut])
async def get_app():
    try:
        return ApplicationService.get_all_apps()
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app_router.delete("/{app_name}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_app(app_name: str):
    try:
        return ApplicationService.remove_app(app_name)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
