import pandas as pd
import re
from models.graph_state import GraphState
from utils.data_utils import filter_csv_with_sql, format_dataframe
from nodes.base_node import BaseNode


class ExecuteSQLNode(BaseNode):
    def execute(self, state):
        response = state["sql_response"]
        trial_num = state.get("trial_num", 0)
        data_source = state["data_source"]
        print(f"<<Trial {trial_num}>>")

        match = re.search(r"<SQL>(.*?)</SQL>", response, re.DOTALL)
        if match:
            sql_query = match.group(1).strip()
        elif trial_num < 3:
            return GraphState(sql_status="retry", trial_num=trial_num + 1)
        else:
            filtered_data = filter_csv_with_sql(
                f"SELECT * FROM {data_source}", self.context.conn
            )
            return GraphState(
                sql_status="generation error", filtered_data=filtered_data
            )

        filtered_data = filter_csv_with_sql(sql_query, self.context.conn)
        print("Filtered data length: ", len(filtered_data))

        if isinstance(filtered_data, pd.DataFrame) and not filtered_data.empty:
            if len(filtered_data) >= 10:
                return GraphState(
                    sql_status="data over 10", filtered_data=filtered_data
                )
            else:
                return GraphState(
                    sql_status="data under 10",
                    filtered_data=format_dataframe(filtered_data, data_source),
                )
        elif trial_num < 3:
            return GraphState(sql_status="retry", trial_num=trial_num + 1)
        else:
            return GraphState(sql_status="no data")
