from langchain_core.prompts import ChatPromptTemplate
from models.graph_state import GraphState
from models.response_schema import RouteQuery
from nodes.base_node import BaseNode
from configs.prompts import SOURCE_ROUTING_PROMPT


class SelectDataNode(BaseNode):
    def execute(self, state):
        chatllm = self.context.llm
        question = state["question"]

        structured_llm = chatllm.with_structured_output(RouteQuery)

        prompt = ChatPromptTemplate.from_messages(
            [("system", SOURCE_ROUTING_PROMPT), ("human", "{question}")]
        )

        # Define router
        router = prompt | structured_llm

        response = router.invoke(question)
        print(response.datasource)
        return GraphState(data_source=response.datasource)
