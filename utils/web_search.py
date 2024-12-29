from typing import Dict
import os

from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import SerpAPIWrapper


def web_search(template: str, serpapi_params: Dict[str, str], query: str, llm) -> str:

    prompt = PromptTemplate(
        template=template,
        input_variables=["query"],
    )

    llm_chain = prompt | llm

    search = SerpAPIWrapper(
        serpapi_api_key=os.getenv("SERPAPI_API_KEY"),
        params=serpapi_params,
    )

    search_results = search.run(query)
    output = llm_chain.invoke(search_results)
    return output
