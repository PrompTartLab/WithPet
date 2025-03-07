from .base_node import BaseNode

from ..modules.graph_state import GraphState


class GetExampleNode(BaseNode):
    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        data_source = state["data_source"]
        question = state["question"]

        examples_topk = self.context.vs_example.similarity_search(
            question,
            k=10,
            filter={"source": data_source},
        )
        examples_format = "\n\n".join(
            [
                f'<QUESTION> {doc.metadata["question"]} </QUESTION>\n<SQL> {doc.metadata["sql"]} </SQL>'
                for doc in examples_topk[:5]
            ]
        )
        return GraphState(examples=examples_format)
