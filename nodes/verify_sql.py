from models.graph_state import GraphState
from nodes.base_node import BaseNode
from utils.data_utils import filter_csv_with_sql
import pandas as pd
import re

columns = {
    "pet_places": [
        "FACILITY_NM",
        "ROAD_NAME_ADDRESS",
        "LAND_LOT_ADDRESS",
        "TEL_NO",
        "HOMEPAGE_URL",
        "HOLIDAY_INFORMATION",
        "OPERATION_TIME_DISPLAY",
        "PARKING_LOT_YN",
        "USAGE_PRICE",
        "POSIBLE_PET_SIZE",
        "PET_LIMIT",
        "PET_POSSIBLE_AT_INDOOR",
        "PET_POSSIBLE_AT_OUTDOOR",
        "FACILITY_INFORMATION",
        "ADDITIONAL_CHARGE_ON_PET",
    ]
}


class VerifySQLNode(BaseNode):
    def execute(self, state: GraphState) -> GraphState:
        response = state["sql_response"]
        data_source = state["data_source"]

        inputs = {"response": response, "data_source": data_source}

        # tracer가 있는 경우 직접 추적 시작
        node_run_id = self._trace_node(inputs) if self.tracer else None

        try:
            match = re.search(r"<SQL>(.*?)</SQL>", response, re.DOTALL)
            if match:
                sql_query = match.group(1).strip()
            else:
                result = GraphState(sql_status="retry")

                if node_run_id:
                    self._end_trace(node_run_id, {"result": result})
                return result

            filtered_data = filter_csv_with_sql(sql_query, self.context.conn)
            print("Data Length: ", len(filtered_data))

            if isinstance(filtered_data, pd.DataFrame) and not filtered_data.empty:
                result = GraphState(
                    sql_status="data exists",
                    filtered_data=filtered_data[columns[data_source]]
                    .head()
                    .to_markdown(index=False),
                )
            else:
                result = GraphState(sql_status="no data")

            if node_run_id:
                self._end_trace(node_run_id, {"result": result})

            return result

        except Exception as e:
            if node_run_id:
                self._end_trace(node_run_id, {"error": str(e)}, status="error")
            raise e
