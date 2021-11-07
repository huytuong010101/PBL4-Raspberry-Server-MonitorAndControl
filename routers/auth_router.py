from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from services.AuthService import AuthService
from pydantics.Token import Token

auth_router = APIRouter(tags=["Authentication"])


@auth_router.post("", response_model=Token)
async def create_token(form_data: OAuth2PasswordRequestForm = Depends()):
    token = None
    try:
        token = AuthService.create_token(form_data.username, form_data.password)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return token



