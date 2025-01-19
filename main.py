from workflows.sql_workflow import SQLWorkflow
from models.graph_state import GraphState
from models.llm import CHATLLM, BASELLM
from utils.data_utils import load_csv_to_sqlite
from configs.examples import EXAMPLES
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from dotenv import load_dotenv
import os
import pandas as pd

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
        question="강화도에 있는 반려 동반 추가 요금 없는 펜션 알려주세요",
    )

    result = app.invoke(initial_state)
    print("Final Answer:\n", result["answer"])


if __name__ == "__main__":
    main()
