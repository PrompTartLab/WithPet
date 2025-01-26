from models.graph_state import GraphState
from configs.schemas import SCHEMAS
from configs.knowledge import busan_general_knowledge
from configs.prompts import SQL_GENERATION_TEMPLATE
from nodes.base_node import BaseNode


class GenerateSQLNode(BaseNode):
    def execute(self, state):
        chatllm = self.context.llm
        data_source = state["data_source"]
        question = state["question"]
        examples = state["examples"]
        schema = SCHEMAS.get(data_source, {})

        sql_chain = SQL_GENERATION_TEMPLATE | chatllm
        response = sql_chain.invoke(
            {
                "question": question,
                "data_source": data_source,
                "examples": examples,
                "schema": schema,
                "external_knowledge": busan_general_knowledge,
            }
        )

        print('\n', response.content)
        return GraphState(schema=schema, sql_response=response.content)
