import ast
import datetime
from http import HTTPStatus
from typing import List

from fastapi import FastAPI, Depends

from src.db import async_session

from src.auth.auth import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.auth.user_models import User

from src.forms.form_models import FormModel, Form, FormCreateModel
from src.forms.CRUD import CRUD_forms
from src.user_responses.CRUD import CRUD_resp
from src.user_responses.response_models import ResponseCreateModel, Response, ResponseModel

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
db_form = CRUD_forms()
db_resp = CRUD_resp()


@app.get("/forms/all", response_model=List[FormModel], tags=["forms"])
async def get_all_forms():
    forms = await db_form.get_all(async_session)

    return forms


@app.post("/forms/create", status_code=HTTPStatus.CREATED, tags=["forms"])
async def create_form(form_data: FormCreateModel, user: User = Depends(current_user)):
    form_data_json = ast.literal_eval(form_data.model_dump_json())

    new_form = Form(
        user_id=user.id,
        form_name=form_data_json["form_name"],
        questions=form_data_json["questions"]
    )

    form = await db_form.add(async_session, new_form)

    return form


@app.get("/forms/{form_id}", tags=["forms"])
async def get_form_by_id(form_id):
    form = await db_form.get_by_id(async_session, int(form_id))

    return form


@app.get("/forms/all/{user_id}", response_model=List[FormModel], tags=["forms"])
async def get_all_forms_made_by_user(user_id):
    forms = await db_form.get_all_forms_by_userid(async_session, int(user_id))

    return forms


@app.patch("/forms/{form_id}/update", tags=["forms"])
async def update_form(form_id, form_data: FormCreateModel, user: User = Depends(current_user)):
    form_data_json = ast.literal_eval(form_data.model_dump_json())

    form = await db_form.update(async_session, int(form_id), form_data_json, user.id)

    return form


@app.delete("/forms/{form_id}/delete", tags=["forms"])
async def delete_form(form_id, user: User = Depends(current_user)):
    form = await db_form.get_by_id(async_session, int(form_id))

    result = await db_form.delete(async_session, form, user.id)

    return result


@app.post("/forms/{form_id}/responses/create",status_code=HTTPStatus.CREATED, tags=["responses"])
async def create_response(response_data: ResponseCreateModel, form_id, user: User = Depends(current_user)):
    response_json = ast.literal_eval(response_data.model_dump_json())

    new_response = Response(
        user_id=user.id,
        form_id = int(form_id),
        resp_date = datetime.datetime.utcnow(),
        choices=response_json["choices"]
    )

    form = await db_resp.add(async_session, new_response, user.id)

    return form


@app.get("/forms/{form_id}/responses/all", response_model=List[ResponseModel], tags=["responses"])
async def get_all_responses_by_form_id(form_id, user: User = Depends(current_user)):
    responses = await db_resp.get_all_by_form_id(async_session, int(form_id), user.id)

    return responses


@app.get("/forms/{form_id}/responses/{user_id}", response_model=ResponseModel, tags=["responses"])
async def get_response_by_form_id_and_user_id(form_id, user_id, user: User = Depends(current_user)):
    response = await db_resp.get_response_by_form_and_user_ids(async_session, int(form_id), int(user_id), user.id)

    return response


@app.patch("/forms/{form_id}/responses/update", tags=["responses"])
async def update_response(form_id, response_data: ResponseCreateModel, user: User = Depends(current_user)):
    response_data_json = ast.literal_eval(response_data.model_dump_json())

    response = await db_resp.update(async_session, int(form_id), response_data_json, user.id)

    return response


@app.delete("/forms/{form_id}/responses/delete", tags=["responses"])
async def delete_response(form_id, user: User = Depends(current_user)):
    response = await db_resp.get_response_by_form_and_user_ids(async_session, int(form_id), user.id, user.id)

    result = await db_resp.delete(async_session, response, user.id)

    return result


@app.get("/users/{user_id}/form_responses", response_model=List[ResponseModel], tags=["SUPERUSER_only"])
async def get_all_responses_by_user_id_SUPERUSER(user_id, user: User = Depends(current_user)):
    responses = await db_resp.get_all_by_user_id(async_session, int(user_id), user)

    return responses
