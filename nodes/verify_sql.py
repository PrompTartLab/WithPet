from models.graph_state import GraphState
from nodes.base_node import BaseNode
from utils.data_utils import filter_csv_with_sql
import pandas as pd
import re


class VerifySQLNode(BaseNode):
    def execute(self, state: GraphState) -> GraphState:
        response = state["sql_response"]

        match = re.search(r"<SQL>(.*?)</SQL>", response, re.DOTALL)
        if match:
            sql_query = match.group(1).strip()
        else:
            return GraphState(sql_status="retry")

        filtered_data = filter_csv_with_sql(sql_query, self.context.conn)
        print("Data Length: ", len(filtered_data))

        if isinstance(filtered_data, pd.DataFrame) and not filtered_data.empty:
            return GraphState(
                sql_status="data exists",
                filtered_data=filtered_data.head().to_markdown(index=False),
            )
        else:
            return GraphState(sql_status="no data")
