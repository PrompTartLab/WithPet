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
    "data/TOURIST_SPOTS.csv": "TOURIST_SPOTS",
    "data/RESTAURANTS.csv": "RESTAURANTS",
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

    documents = []
    df = pd.read_csv("./data/RESTAURANTS.csv")
    df["SOURCE"] = "restaurants"
    for _, row in df.iterrows():
        # Combine the columns to embed into a single string (if needed)
        content = "\n".join([f"{col}: {str(row[col])}" for col in ["REVIEW"]])

        # Save other columns as metadata
        metadata = {
            col: row[col]
            for col in df.columns
            if col
            in [
                "RESTAURANT_NAME_KOREAN",
                "FOOD_TYPE",
                "ADDRESS_KOREAN",
                "MENU_NAME",
                "NATIONAL_PHONE_NUMBER",
                "BREAKFAST_YN",
                "LUNCH_YN",
                "DINNER_YN",
                "BEER_YN",
                "OUTDOOR_SEAT_YN",
                "MENU_FOR_CHILDREN_YN",
                "RESTROOM_YN",
                "PARKING_LOT_YN" "DISTRICT",
                "RESTAURANT_NAME_ENGLISH",
                "ADDRESS_ENGLISH",
                "SOURCE",
                "INDEX",
            ]
        }

        # Create a Document object
        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)

    df = pd.read_csv("./data/TOURIST_SPOTS.csv")
    df["SOURCE"] = "tourist_spots"
    for _, row in df.iterrows():
        # Combine the columns to embed into a single string (if needed)
        content = "\n".join([f"{col}: {str(row[col])}" for col in ["DESCRIPTION"]])

        # Save other columns as metadata
        metadata = {
            col: row[col]
            for col in df.columns
            if col in ["PLACE_NM", "ADDRESS", "TEL_NO", "SOURCE", "INDEX"]
        }

        # Create a Document object
        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)

    vectorstore_data = FAISS.from_documents(documents, embeddings)

    tour_rag = SQLWorkflow(
        CHATLLM, CHATLLM, conn, vectorstore_examples, vectorstore_data
    )
    app = tour_rag.setup_workflow()

    initial_state = GraphState(
        question="광안리 근처 사진찍기 좋은 곳 추천해주세요",
    )

    result = app.invoke(initial_state)
    print("Final Answer:", result["answer"])


if __name__ == "__main__":
    main()
