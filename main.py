from workflows.sql_workflow import SQLWorkflow
from models.graph_state import GraphState
from models.llm import CHATLLM, BASELLM
from utils.data_utils import load_csv_to_sqlite
from configs.examples import EXAMPLES
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langgraph.errors import GraphRecursionError
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

csv_files = {
    "data/PET_PLACES.csv": "PET_PLACES",
}


def main():

    conn = load_csv_to_sqlite(csv_files)
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    questions = [item["question"] for item in EXAMPLES]
    question_embeddings = [
        (question, embeddings.embed_query(question)) for question in questions
    ]
    vectorstore_examples = FAISS.from_embeddings(
        text_embeddings=question_embeddings, embedding=embeddings, metadatas=EXAMPLES
    )

    tour_rag = SQLWorkflow(
        CHATLLM, CHATLLM, conn, vectorstore_examples
    )
    app = tour_rag.setup_workflow()

    initial_state = GraphState(
        question="종로구에 무료 주차되는 카페 알려줘",
    )


    try:
        result = app.invoke(initial_state, {"recursion_limit": 7})
        print('\n', result["answer"])
    except GraphRecursionError:
        print("에러가 발생했습니다. 다시 시도해주세요.")


if __name__ == "__main__":
    main()
