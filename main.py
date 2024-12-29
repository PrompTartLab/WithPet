from workflows.sql_workflow import SQLWorkflow
from models.graph_state import GraphState
from models.llm import CHATLLM, BASELLM

def main():

    tour_rag = SQLWorkflow(CHATLLM, BASELLM)
    app = tour_rag.app

    initial_state = GraphState(
        question="광안리 근처 사진찍기 좋은 곳 추천해주세요",
    )

    result = app.invoke(initial_state)
    print("Final Answer:", result['answer'])

if __name__ == "__main__":
    main()
