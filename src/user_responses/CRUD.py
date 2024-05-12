import datetime

from fastapi import HTTPException

from src.user_responses.response_models import Response
from src.forms.form_models import Form
from src.auth.user_models import User

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select

types_matching = {"scq": "int", "mcq": "List[int]", "tfq": "str"}


class CRUD_resp:
    async def add(self, async_session: async_sessionmaker[AsyncSession], response: Response, user_id):
        async with async_session() as session:
            statement = select(Form).filter(Form.id == response.form_id)
            statement1 = select(Response).filter(Response.form_id == response.form_id, Response.user_id == user_id)

            check = await session.execute(statement1)
            result = await session.execute(statement)

            if check.first() is not None:
                raise HTTPException(status_code=422, detail="You already sent a response to this form,"
                                                            " use 'Update' instead.")
            form = result.scalars().one()

            for num, question in form.questions.items():
                q_type = question["q_type"]

                match q_type:
                    case "scq":
                        if not isinstance(response.choices[num], int):
                            raise HTTPException(status_code=422, detail=f"Wrong input for question number {num}, "
                                                                        f"answer must be of type {types_matching[q_type]}")
                    case "mcq":
                        if not isinstance(response.choices[num], list):
                            raise HTTPException(status_code=422, detail=f"Wrong input for question number {num}, "
                                                                        f"answer must be of type {types_matching[q_type]}")
                    case "tfq":
                        if not isinstance(response.choices[num], int):
                            raise HTTPException(status_code=422, detail=f"Wrong input for question number {num}, "
                                                                        f"answer must be of type {types_matching[q_type]}")

            session.add(response)
            await session.commit()

        return response

    async def get_response_by_form_and_user_ids(self, async_session: async_sessionmaker[AsyncSession], form_id, user_id, cur_usr_id):
        async with async_session() as session:
            statement = select(Response).filter(Response.form_id == form_id, Response.user_id == user_id)
            statement_formcheck = select(Form).filter(Form.id == form_id)

            result = await session.execute(statement)
            result1 = await session.execute(statement_formcheck)

            response = result.scalars().one()
            response_check = result1.scalars().one()

            if response.user_id != cur_usr_id and response_check.user_id != cur_usr_id:
                raise HTTPException(status_code=403, detail="Authentication failed. Access denied.")
            else:
                return response

    async def get_all_by_form_id(self, async_session: async_sessionmaker[AsyncSession], form_id, cur_usr_id):
        async with async_session() as session:
            statement = select(Response).filter(Response.form_id == form_id)
            statement_formcheck = select(Form).filter(Form.id == form_id)

            result = await session.execute(statement)
            result1 = await session.execute(statement_formcheck)

            form = result1.scalars().one()

            if form.user_id != cur_usr_id:
                raise HTTPException(status_code=403, detail="You are not this form's creator."
                                                            "Response list request denied.")
            else:
                return result.scalars()

    async def get_all_by_user_id(self, async_session: async_sessionmaker[AsyncSession], user_id, user):
        async with async_session() as session:
            statement = select(Response).filter(Response.user_id == user_id)

            result = await session.execute(statement)

            if not user.is_superuser:
                raise HTTPException(status_code=403, detail="Only superuser is allowed to do that.")
            else:
                return result.scalars()

    async def update(self, async_session: async_sessionmaker[AsyncSession], form_id, data, user_id):
        async with async_session() as session:
            statement = select(Response).filter(Response.form_id == form_id, Response.user_id == user_id)

            result = await session.execute(statement)

            response = result.scalars().one()

            if user_id != response.user_id:
                raise HTTPException(status_code=403, detail="You are not this response's creator."
                                                            "Update request denied.")
            else:
                response.choices = data["choices"]

                await session.commit()

                return response

    async def delete(self, async_session: async_sessionmaker[AsyncSession], response: Response, user_id):
        async with async_session() as session:
            if user_id != response.user_id:
                raise HTTPException(status_code=403, detail="You are not this form's creator. Delete request denied.")
            else:
                await session.delete(response)
                await session.commit()

                return {}
