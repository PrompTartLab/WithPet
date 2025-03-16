from typing import TypedDict
import pandas as pd


class GraphState(TypedDict):
    question: str
    data_source: str
    schema: str
    examples: str
    generated_sql: str
    sql_status: str
    filtered_data: pd.DataFrame
    refined_question: str
    formatted_data: str
    web_response: str
    answer: str
