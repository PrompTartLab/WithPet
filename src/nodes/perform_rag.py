import pandas as pd

from .base_node import BaseNode

from ..modules.graph_state import GraphState


class PerformRAGNode(BaseNode):
    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        query = state["refined_question"]
        data_source = state["data_source"]
        filtered_data_list = state["filtered_data"]

        # 리스트에서 INDEX 값만 추출
        index_values = [
            item.get("INDEX") for item in filtered_data_list if "INDEX" in item
        ]

        retrieved_data = self.context.vs_data.similarity_search(
            query,
            k=5,
            filter={
                "SOURCE": data_source,
                "INDEX": {"$in": index_values},
            },
        )
        retrieved_index = [res.metadata["INDEX"] for res in retrieved_data]
        print("Retrieved data Length: ", len(retrieved_index))

        filtered_df = pd.DataFrame(filtered_data_list)

        return GraphState(
            formatted_data=filtered_df[filtered_df["INDEX"].isin(retrieved_index)]
            .head()
            .to_markdown(index=False),
        )
