from models.graph_state import GraphState
from nodes.base_node import BaseNode


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
        final_query = f"""
            Based on the user's question: {question}
            From the table with schema:
            {schema}
            Retrieved information is:
            {data}
            Please provide a detailed and concise answer in Korean.
            The data may not match the question completely. If so, please explain the content of the retrieved data, but notify that it may not match the question.
            """
        final_answer = chatllm.invoke(final_query)
        answer = final_answer if type(final_answer) == str else final_answer.content

        return GraphState(answer=answer)

class HandleNotRelevantNode(BaseNode):
    def execute(self, state):
        return GraphState(answer="해당 질문은 이 챗봇 가이드에서 대답드릴 수 없습니다. 반려동물 동반 가능한 시설에 대해 질문해주세요.")

class HandleNoDataNode(BaseNode):
    def execute(self, state):
        chatllm = self.context.llm_stream
        question = state["question"]
        final_query = f"""
            Based on the user's question: {question}
            You did not retrieve the relevant data.
            Please write the new request in Korean for asking another question.
            """
        answer = final_answer if type(final_answer) == str else final_answer.content

        return GraphState(answer=answer)
