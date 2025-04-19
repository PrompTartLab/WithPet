from typing import Dict

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import SerpAPIWrapper

from .base_node import BaseNode

from ..modules.graph_state import GraphState


class WebSearchNode(BaseNode):
    def __init__(
        self,
        translate_template: str,
        search_template: str,
        serpapi_api_key: str,
        serpapi_params: Dict[str, str],
    ) -> None:
        super().__init__()
        self.translate_template = translate_template
        self.search_template = search_template
        self.serpapi_api_key = serpapi_api_key
        self.serpapi_params = serpapi_params

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        llm = self.context.llm
        query = state["question"]

        translated = self.ko_to_eng(
            query=query,
            llm=llm,
        )

        output = self.web_search(
            query=translated,
            llm=llm,
        )
        print(output)
        return GraphState(web_response=output.content)

    def ko_to_eng(
        self,
        query: str,
        llm: ChatOpenAI,
    ) -> str:
        prompt = PromptTemplate(
            template=self.translate_template,
            input_variables=["query"],
        )

        llm_chain = prompt | llm

        output = llm_chain.invoke(query)
        return output

    def web_search(
        self,
        query: str,
        llm: ChatOpenAI,
    ) -> str:
        prompt = PromptTemplate(
            template=self.search_template,
            input_variables=["query"],
        )

        llm_chain = prompt | llm

        search = SerpAPIWrapper(
            serpapi_api_key=self.serpapi_api_key,
            params=self.serpapi_params,
        )

        search_results = search.run(query)
        output = llm_chain.invoke(search_results)
        return output
