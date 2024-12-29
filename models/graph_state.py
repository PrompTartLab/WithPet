from typing import TypedDict


class GraphState(TypedDict):
    question: str
    data_source: str
    sql_response: str
    sql_status: str
    trial_num: int
    data: str
    web_response: str
    answer: str
