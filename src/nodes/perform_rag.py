from .base_node import BaseNode

from ..modules.graph_state import GraphState


class PerformRAGNode(BaseNode):
    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        question = state["question"]
        data_source = state["data_source"]
        filtered_data = state["filtered_data"]
        print(filtered_data["INDEX"].to_list())
        retrieved_data = self.context.vs_data.similarity_search(
            question,
            k=5,
            filter={
                "SOURCE": data_source,
                "INDEX": {"$in": filtered_data["INDEX"].to_list()},
            },
        )
        retrieved_index = [res.metadata["INDEX"] for res in retrieved_data]
        print("Retrieved data Length: ", len(retrieved_index))
        return GraphState(
            formatted_data=filtered_data[filtered_data["INDEX"].isin(retrieved_index)]
            .head()
            .to_markdown(index=False),
        )
