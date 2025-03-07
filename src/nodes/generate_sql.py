from typing import Dict

from langchain_core.prompts import PromptTemplate

from .base_node import BaseNode

from ..modules.context import Context
from ..modules.graph_state import GraphState


class GenerateSQLNode(BaseNode):
    def __init__(
        self,
        context: Context,
        schemas: Dict[str, str],
        sql_generation_template: PromptTemplate,
    ) -> None:
        super().__init__(context=context)
        self.schemas = schemas
        self.sql_generation_template = sql_generation_template

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        llm = self.context.llm
        data_source = state["data_source"]
        question = state["question"]
        examples = state["examples"]
        schema = self.schemas.get(
            data_source,
            {},
        )

        sql_chain = self.sql_generation_template | llm
        response = sql_chain.invoke(
            {
                "question": question,
                "data_source": data_source,
                "examples": examples,
                "schema": schema,
                "external_knowledge": "",
            }
        )

        return GraphState(
            schema=schema,
            sql_response=response.content,
        )
