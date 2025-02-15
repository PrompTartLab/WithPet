import pandas as pd
import re
from models.graph_state import GraphState
from utils.data_utils import format_docs_with_metadata, format_dataframe
from nodes.base_node import BaseNode


class PerformRAGNode(BaseNode):
    def execute(self, state):
        question = state["question"]
        data_source = state["data_source"]
        filtered_data = state["filtered_data"]

        inputs = {
            "question": question,
            "data_source": data_source,
            "filtered_data": filtered_data,
        }

        # tracer가 있는 경우 직접 추적 시작
        node_run_id = self._trace_node(inputs) if self.tracer else None

        try:
            retriever = self.context.vs_data.as_retriever(
                search_kwargs={
                    "k": 10,
                    "filter": {
                        "SOURCE": data_source,
                        "INDEX": filtered_data["INDEX"].to_list(),
                    },
                }
            )
            results = retriever.invoke(question)

            if len(results) == 0:
                result = GraphState(
                    rag_filtered_data=format_dataframe(
                        filtered_data.head(5), data_source
                    )
                )
            else:
                rag_filtered_data = format_docs_with_metadata(results)
                result = GraphState(filtered_data=rag_filtered_data)

            # 결과 추적 기록
            if node_run_id:
                self._end_trace(node_run_id, {"result": result})

            return result

        except Exception as e:
            if node_run_id:
                self._end_trace(node_run_id, {"error": str(e)}, status="error")
            raise e
