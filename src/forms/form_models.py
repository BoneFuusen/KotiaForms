from typing import List, Union, Dict
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Integer, String, MetaData, ForeignKey, JSON
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship

from src.db import Base
from src.auth.user_models import User


class Question(BaseModel):
    q_type: str
    q_text: str
    choices: List[str]


class FormModel(BaseModel):
    id: int
    user_id: int
    form_name: str
    questions: Dict[int, Question]

    model_config = ConfigDict(
        from_attributes=True
    )


class FormCreateModel(BaseModel):
    form_name: str
    questions: Dict[int, Question]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "form_name": "Sample_name",
            "questions": {
                "qnum": {
                    "q_type": "sample_type",
                    "q_text": "sample qtext",
                    "choices": ["sometext", "sometext1"]
                        }
            }
        }
    )


metadata = MetaData()


class Form(Base):
    __tablename__ = "form"
    metadata = metadata

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(User.id), nullable=False, index=True
    )
    form_name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    questions = mapped_column(JSON, nullable=False)

    user_relationship = relationship("User")
