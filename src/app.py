import ast
from http import HTTPStatus
from typing import List

from fastapi import FastAPI, Depends

from src.db import async_session

from src.auth.auth import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.auth.user_models import User

from src.forms.form_models import FormModel, Form, FormCreateModel
from src.forms.CRUD import CRUD

app = FastAPI(
    title="KotiaForms"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

current_user = fastapi_users.current_user(active=True)


@app.get("/auth/current-user", tags=["cur_usr"])
async def get_current_user(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


async_session = async_session
db = CRUD()


@app.get("/form/all", response_model=List[FormModel], tags=["forms"])
async def get_all_forms():
    forms = await db.get_all(async_session)

    return forms


@app.post("/form/create", status_code=HTTPStatus.CREATED, tags=["forms"])
async def create_form(form_data: FormCreateModel, user: User = Depends(current_user)):
    form_data_json = ast.literal_eval(form_data.model_dump_json())

    new_form = Form(
        user_id=user.id,
        form_name=form_data_json["form_name"],
        questions=form_data_json["questions"]
    )

    form = await db.add(async_session, new_form)

    return form


@app.get("/form/{form_id}", tags=["forms"])
async def get_form_by_id(form_id):
    form = await db.get_by_id(async_session, int(form_id))

    return form


@app.patch("/form/{form_id}", tags=["forms"])
async def update_form(form_id, form_data: FormCreateModel, user: User = Depends(current_user)):
    form_data_json = ast.literal_eval(form_data.model_dump_json())

    form = await db.update(async_session, int(form_id), form_data_json, user.id)

    return form


@app.delete("/form/{form_id}", tags=["forms"])
async def delete_form(form_id, user: User = Depends(current_user)):
    form = await db.get_by_id(async_session, int(form_id))

    result = await db.delete(async_session, form, user.id)

    return result
