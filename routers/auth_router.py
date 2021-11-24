from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from services.AuthService import AuthService
from pydantics.Token import Token
from threading import Thread
from models.LoginLog import LoginLog
from datetime import datetime
auth_router = APIRouter(tags=["Authentication"])


@auth_router.post("", response_model=Token)
async def create_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    token = None
    try:
        token = AuthService.create_token(form_data.username, form_data.password)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    try:
        Thread(target=lambda: LoginLog.create(
            user=form_data.username,
            device=request.client.host,
            time=datetime.now()
        )).start()
    except Exception:
        pass
    return token



