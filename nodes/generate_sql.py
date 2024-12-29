from models.graph_state import GraphState
from configs.schemas import schemas
from configs.knowledge import busan_general_knowledge
from configs.prompts import sql_generation_template, sql_retry_template
from nodes.base_node import BaseNode


class GenerateSQLNode(BaseNode):
    def execute(self, state):
        chatllm = self.context.llm
        datasource = state[
            "data_source"
        ]  # Example: 'local_tourist_spots' or 'foreign_tourist_spots'
        question = state["question"]
        sql_status = state.get("sql_status", [])
        schema = schemas.get(datasource, {})

        if sql_status == "retry":
            previous_answer = state["sql_response"]

            sql_chain = sql_retry_template | chatllm
            response = sql_chain.invoke(
                {
                    "question": question,
                    "datasource": datasource,
                    "schema": schema,
                    "external_knowledge": busan_general_knowledge,
                    "previous_answer": previous_answer,
                }
            )
        else:
            sql_chain = sql_generation_template | chatllm
            response = sql_chain.invoke(
                {
                    "question": question,
                    "datasource": datasource,
                    "schema": schema,
                    "external_knowledge": busan_general_knowledge,
                }
            )

        print(response.content)
        return GraphState(sql_response=response.content)
