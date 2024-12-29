from langchain_core.prompts import ChatPromptTemplate
from models.graph_state import GraphState
from models.response_schema import RouteQuery
from nodes.base_node import BaseNode


class SelectDataNode(BaseNode):
    def execute(self, state):
        chatllm = self.context.llm
        question = state["question"]

        structured_llm = chatllm.with_structured_output(RouteQuery)

        # Prompt 정의
        system = """
    You are an expert at routing a user question to the appropriate data source.
    Based on the category the question is referring to, route it to the relevant data source.
    Return "foreign_tourist_spots" if the query asks for recommendation of tourist spots where foreign people like.
    Return "local_tourist_spots" if the query asks for recommendation of tourist spots but there is no foreign-related keyword.
    Return "restaurants" if the query requests restaurant recommendations.
    Returns "web" if it is not related to tourist attractions or restaurants, such as weather or transportation.
        """

        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", "{question}")]
        )

        # Define router
        router = prompt | structured_llm

        response = router.invoke(question)
        return GraphState(data_source=response.datasource)
