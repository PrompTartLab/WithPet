from models.graph_state import GraphState
from nodes.base_node import BaseNode
from utils.data_utils import filter_csv_with_sql, format_dataframe
import pandas as pd
import re

class VerifySQLNode(BaseNode):
    def execute(self, state: GraphState) -> GraphState:
        response = state["sql_response"]    
        trial_num = state.get("trial_num", 0)
        data_source = state["data_source"]
        print(f'<<Trial {trial_num}>>')

        match = re.search(r'<SQL>(.*?)</SQL>', response, re.DOTALL)
        if match:
            sql_query = match.group(1).strip()
        else:
            return GraphState(sql_status = 'retry', trial_num=trial_num+1)

        filtered_data = filter_csv_with_sql(sql_query, self.context.conn)
        print(filtered_data)

        if isinstance(filtered_data, pd.DataFrame) and not filtered_data.empty:
            return GraphState(sql_status = 'data exists', filtered_data=format_dataframe(filtered_data.head(5), data_source))
        elif trial_num < 3:
            return GraphState(sql_status = 'retry', trial_num=trial_num+1)
        else:
            return GraphState(sql_status = 'no data')