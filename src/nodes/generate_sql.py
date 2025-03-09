from langchain_core.prompts import PromptTemplate

from .base_node import BaseNode

from ..modules.context import Context
from ..modules.graph_state import GraphState
from ..modules.response_schema import SQLQuery


class GenerateSQLNode(BaseNode):
    def __init__(
        self,
        context: Context,
        sql_generation_template: PromptTemplate,
    ) -> None:
        super().__init__(context=context)
        self.sql_generation_template = sql_generation_template

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        llm = self.context.llm
        data_source = state["data_source"]
        question = state["question"]
        examples = state["examples"]
        schema = state["schema"]

        structured_llm = llm.with_structured_output(SQLQuery)
        sql_chain = self.sql_generation_template | structured_llm
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
            generated_sql=response.sql,
        )
