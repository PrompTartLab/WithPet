from typing import Literal

from pydantic import BaseModel, Field


class QueryRouter(BaseModel):
    datasource: Literal["pet_places", "not_relevant"] = Field(
        description="Given a user question choose which datasource would be most relevant for answering their question",
    )


class SQLQuery(BaseModel):
    sql: str = Field(
        description="The generated SQL query.",
    )
