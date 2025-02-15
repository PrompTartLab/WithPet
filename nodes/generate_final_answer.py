from models.graph_state import GraphState
from nodes.base_node import BaseNode
from configs.prompts import ANSWER_GENERATION_TEMPLATE


class GenerateAnswerNode(BaseNode):
    def execute(self, state):
        chatllm = self.context.llm_stream
        question = state["question"]
        schema = state["schema"]
        data = (
            state["web_response"]
            if state["data_source"] == "web"
            else state["filtered_data"]
        )

        chain = ANSWER_GENERATION_TEMPLATE | chatllm
        final_answer = chain.invoke(
            {
                "question": question,
                "schema": schema,
                "data": data,
            }
        )
        answer = final_answer if type(final_answer) == str else final_answer.content

        return GraphState(answer=answer)


class HandleNotRelevantNode(BaseNode):
    def execute(self, state):
        return GraphState(
            answer="해당 질문은 이 챗봇 가이드에서 대답드릴 수 없습니다. 반려동물 동반 시설에 대해 질문해주세요."
        )


class HandleNoDataNode(BaseNode):
    def execute(self, state):
        return GraphState(answer="해당 질문에 해당하는 장소를 찾지 못했습니다. 새로운 조건으로 질문해주세요.")
