from models.graph_state import GraphState
from nodes.base_node import BaseNode


class GenerateAnswerNode(BaseNode):
    def execute(self, state):
        chatllm = self.context.llm_stream
        question = state["question"]
        data = state["web_response"] if state["data_source"] == "web" else state["data"]
        final_query = f"""
            Based on the user's question: {question}
            and the following retrieved information:
            {data}
            Please provide a detailed and concise answer in Korean.
            """
        final_answer = chatllm.invoke(final_query)

        return GraphState(answer=final_answer)


class HandleNoDataNode(BaseNode):
    def execute(self, state):
        chatllm = self.context.llm_stream
        question = state["question"]
        final_query = f"""
            Based on the user's question: {question}
            You did not retrieve the relevant data.
            Please write the new request in Korean for asking another question.
            """
        final_answer = chatllm.invoke(final_query)

        return GraphState(answer=final_answer)
