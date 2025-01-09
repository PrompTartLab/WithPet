from models.graph_state import GraphState
from configs.schemas import schemas
from configs.knowledge import busan_general_knowledge
from configs.prompts import SQL_GENERATION_TEMPLATE, SQL_RETRY_TEMPLATE
from nodes.base_node import BaseNode


class GenerateSQLNode(BaseNode):
    def execute(self, state):
        chatllm = self.context.llm
        data_source = state["data_source"]
        question = state["question"]
        examples = state["examples"]
        sql_status = state.get("sql_status", [])
        schema = schemas.get(data_source, {})

        if sql_status == "retry":
            previous_answer = state["sql_response"]

            sql_chain = SQL_RETRY_TEMPLATE | chatllm
            response = sql_chain.invoke(
                {
                    "question": question,
                    "data_source": data_source,
                    "examples": examples,
                    "schema": schema,
                    "external_knowledge": busan_general_knowledge,
                    "previous_answer": previous_answer,
                }
            )
        else:
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

        print(response.content)
        return GraphState(schema=schema, sql_response=response.content)
