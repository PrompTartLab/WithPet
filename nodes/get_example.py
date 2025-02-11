from models.graph_state import GraphState
from nodes.base_node import BaseNode


class GetExampleNode(BaseNode):
    def execute(self, state):
        data_source = state["data_source"]
        question = state["question"]

        inputs = {"data_source": data_source, "question": question}

        # tracer가 있는 경우 직접 추적 시작
        node_run_id = self._trace_node(inputs) if self.tracer else None

        try:
            examples_topk = self.context.vs_example.similarity_search(
                question, k=10, filter={"source": data_source}
            )
            examples_format = "\n\n".join(
                [
                    f'<QUESTION> {doc.metadata["question"]} </QUESTION>\n<SQL> {doc.metadata["sql"]} </SQL>'
                    for doc in examples_topk[:3]
                ]
            )
            print(examples_format)
            result = GraphState(examples=examples_format)

            # 결과 추적 기록
            if node_run_id:
                self._end_trace(node_run_id, {"result": result})

            return result

        except Exception as e:
            if node_run_id:
                self._end_trace(node_run_id, {"error": str(e)}, status="error")
            raise e
