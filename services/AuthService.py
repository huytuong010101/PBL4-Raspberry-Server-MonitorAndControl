from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from utils.auth import AuthUtil
from models.User import User
from models.LoginLog import LoginLog

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)):
        try:
            user = AuthUtil.decode_token(token)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Loggin session is expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    @staticmethod
    def create_token(username, password):
        user = User.get_or_none(username=username)
        if user is None or not AuthUtil.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username and Passowrd is not matching",
                headers={"WWW-Authenticate": "Bearer"}
            )
        token = AuthUtil.create_access_token({
            "sub": username,
            "fullname": user.fullname,
            "is_admin": user.is_admin,
            "avatar": user.avatar
        })

        try:
            LoginLog.create(user=username)
        except Exception:
            pass

        return {"access_token": token, "token_type": "bearer"}


