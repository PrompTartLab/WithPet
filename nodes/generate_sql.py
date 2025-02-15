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

        inputs = {
            "question": question,
            "data_source": data_source,
            "examples": examples,
            "schema": schema,
        }

        # tracer가 있는 경우 직접 추적 시작
        node_run_id = (
            self._trace_node(inputs, SQL_GENERATION_TEMPLATE) if self.tracer else None
        )

        sql_chain = SQL_GENERATION_TEMPLATE | chatllm
        response = sql_chain.invoke(
            {
                "question": question,
                "data_source": data_source,
                "examples": examples,
                "schema": schema,
                "external_knowledge": "",
            }
        )

        print("\n", response.content)
        result = GraphState(schema=schema, sql_response=response.content)

        # 결과 추적 기록
        if node_run_id:
            self._end_trace(node_run_id, {"result": result})

        return result
