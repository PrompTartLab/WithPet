from langchain_core.prompts import ChatPromptTemplate
from models.graph_state import GraphState
from models.response_schema import RouteQuery
from nodes.base_node import BaseNode
from configs.prompts import SOURCE_ROUTING_PROMPT


class SelectDataNode(BaseNode):
    def execute(self, state):
        chatllm = self.context.llm
        question = state["question"]

        inputs = {"question": question}

        # tracer가 있는 경우 직접 추적 시작
        node_run_id = (
            self._trace_node(inputs, SOURCE_ROUTING_PROMPT) if self.tracer else None
        )

        try:
            structured_llm = chatllm.with_structured_output(RouteQuery)
            prompt = ChatPromptTemplate.from_messages(
                [("system", SOURCE_ROUTING_PROMPT), ("human", "{question}")]
            )
            router = prompt | structured_llm
            response = router.invoke(question)

            result = GraphState(data_source=response.datasource)

            # 결과 추적 기록
            if node_run_id:
                self._end_trace(node_run_id, {"result": result})

            return result

        except Exception as e:
            if node_run_id:
                self._end_trace(node_run_id, {"error": str(e)}, status="error")
            raise e
