from typing import TypedDict
import pandas as pd


class GraphState(TypedDict):
    question: str
    data_source: str
    schema: str
    examples: str
    generated_sql: str
    sql_status: str
    trial_num: int
    filtered_data: pd.DataFrame
    formatted_data: str
    web_response: str
    answer: str
