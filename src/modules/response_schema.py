from typing import Literal

from pydantic import BaseModel, Field


class QueryRouter(BaseModel):
    datasource: Literal["PET_PLACES", "NOT_RELEVANT"] = Field(
        description="Given a user question choose which datasource would be most relevant for answering their question",
    )


class SQLQuery(BaseModel):
    sql: str = Field(
        description="The generated SQL query without any explanation.",
    )


class RefinedQuestion(BaseModel):
    question: str = Field(
        description="The refined user question based on the requirements.",
    )
