from typing import Dict, List

import re

import pandas as pd

from .base_node import BaseNode

from ..modules.context import Context
from ..modules.graph_state import GraphState
from ..utils.data_utils import filter_csv_with_sql


class VerifySQLNode(BaseNode):
    def __init__(
        self,
        context: Context,
        source_columns: Dict[str, List[str]],
    ) -> None:
        super().__init__(context=context)
        self.source_columns = source_columns

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        response = state["sql_response"]
        data_source = state["data_source"]

        match = re.search(
            r"<SQL>(.*?)</SQL>",
            response,
            re.DOTALL,
        )
        if match:
            sql_query = match.group(1).strip()
        else:
            return GraphState(sql_status="retry")

        filtered_data = filter_csv_with_sql(
            query=sql_query,
            conn=self.context.conn,
        )
        if isinstance(filtered_data, pd.DataFrame) and not filtered_data.empty:
            print("Data Length: ", len(filtered_data))
            columns_to_show = [
                column
                for column in filtered_data.columns
                if column in self.source_columns[data_source]
            ]
            return GraphState(
                sql_status="data exists",
                filtered_data=filtered_data[columns_to_show]
                .head()
                .to_markdown(index=False),
            )
        else:
            print(filtered_data)
            return GraphState(sql_status="no data")
