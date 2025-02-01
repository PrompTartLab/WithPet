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
        print(results)
        if len(results) == 0:
            return GraphState(
                rag_filtered_data=format_dataframe(filtered_data.head(5), data_source)
            )
        rag_filtered_data = format_docs_with_metadata(results)
        return GraphState(filtered_data=rag_filtered_data)
