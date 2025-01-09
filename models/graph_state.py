from typing import TypedDict


class GraphState(TypedDict):
    question: str
    data_source: str
    schema: str
    examples: str
    sql_response: str
    sql_status: str
    trial_num: int
    sql_filtered_data: str
    rag_filtered_data: str
    web_response: str
    answer: str
