from typing import TypedDict


class GraphState(TypedDict):
    question: str
    data_source: str
    schema: str
    examples: str
    generated_sql: str
    sql_status: str
    trial_num: int
    filtered_data: str
    web_response: str
    answer: str
