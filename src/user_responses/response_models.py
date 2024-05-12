import datetime
from typing import Dict, List

from pydantic import BaseModel, ConfigDict
from sqlalchemy import MetaData, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base
from src.auth.user_models import User
from src.forms.form_models import Form


class ResponseModel(BaseModel):
    id: int
    user_id: int
    form_id: int
    resp_date: datetime.datetime
    choices: Dict[int, int | List[int] | str]

    model_config = ConfigDict(
        from_attributes=True
    )


class ResponseCreateModel(BaseModel):
    choices: Dict[int, int | List[int] | str]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "choices": {
                "q_num1": "integer/single_choice",
                "q_num2": "[integer]/multiple_choice",
                "q_num3": "string/text_field"
            }
        }
    )


metadata = MetaData()


class Response(Base):
    __tablename__ = "response"
    metadata = metadata

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(User.id), nullable=False, index=True
    )
    form_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Form.id), nullable=False, index=True
    )
    resp_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, index=True
    )
    choices = mapped_column(
        JSON, nullable=False
    )

    user_relationship = relationship("User")
    form_relationship = relationship("Form")
