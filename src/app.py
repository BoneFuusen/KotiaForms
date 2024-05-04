from fastapi import FastAPI, Depends

from src.auth.auth import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.auth.user_models import User

app = FastAPI(
    title="KotiaForms"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

