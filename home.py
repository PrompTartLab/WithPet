import streamlit as st
import os

from langchain_openai import OpenAI, OpenAIEmbeddings
from models.llm import CHATLLM
from workflows.sql_workflow import SQLWorkflow
from utils.data_utils import load_csv_to_sqlite
from configs.examples import EXAMPLES
from langchain.callbacks.base import BaseCallbackHandler
from langchain.vectorstores import FAISS
from langchain_core.tracers import LangChainTracer
from langchain.callbacks.manager import CallbackManager


# OpenAI API 키 로드
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Langsmith tracing을 위한 키 로드
LANGCHAIN_API_KEY = st.secrets["LANGCHAIN_API_KEY"]
LANGCHAIN_PROJECT = st.secrets["LANGCHAIN_PROJECT"]
LANGCHAIN_TRACING_V2 = "true"
LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"

# 페이지 설정
st.set_page_config(page_title="TourGuideRAG", page_icon="🎡")

# 메시지 세션 스테이트 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []


class ChatCallbackHandler(BaseCallbackHandler):
    """
    LLM이 토큰 단위로 출력할 때마다 Streamlit UI에 실시간 업데이트해주는 콜백 핸들러입니다.
    """

    message = ""

    def on_llm_start(self, *args, **kwargs):
        """LLM이 시작될 때 호출됩니다. 토큰 누적용 빈 컨테이너를 만듭니다."""
        self.message_box = st.empty()

    def on_llm_end(self, *args, **kwargs):
        """LLM이 종료될 때 호출됩니다. 최종 메시지를 저장합니다."""
        save_message(self.message, "ai")

    def on_llm_new_token(self, token, *args, **kwargs):
        """LLM이 새 토큰을 생성할 때마다 호출됩니다. 토큰을 누적해 UI에 표시합니다."""
        self.message += token
        self.message_box.markdown(self.message)


def save_message(message: str, role: str) -> None:
    """메시지를 세션 스테이트에 저장합니다."""
    st.session_state["messages"].append({"message": message, "role": role})


def send_message(message: str, role: str, save: bool = True) -> None:
    """
    채팅 UI에 메시지를 출력합니다.
    save=True인 경우, 세션 스테이트에도 메시지를 저장합니다.
    """
    with st.chat_message(role):
        st.markdown(message)
    if save:
        save_message(message, role)


def paint_history() -> None:
    """세션 스테이트에 기록된 메시지를 모두 다시 출력합니다."""
    for msg in st.session_state["messages"]:
        send_message(msg["message"], msg["role"], save=False)


@st.cache_resource
def get_sqlite_connection(csv_files):
    return load_csv_to_sqlite(csv_files)


@st.cache_resource
def get_embeddings(api_key):
    return OpenAIEmbeddings(openai_api_key=api_key)


@st.cache_resource
def get_vectorstore_examples(examples, OPENAI_API_KEY):
    questions = [item["question"] for item in examples]
    embeddings = get_embeddings(OPENAI_API_KEY)
    question_embeddings = [
        (question, embeddings.embed_query(question)) for question in questions
    ]
    vectorstore = FAISS.from_embeddings(
        text_embeddings=question_embeddings, embedding=embeddings, metadatas=examples
    )
    return vectorstore


tracer = LangChainTracer(project_name=LANGCHAIN_PROJECT)
callback_manager = CallbackManager([tracer])

csv_files = {
    "./data/pet_places.csv": "pet_places",
}

# LLM 인스턴스 준비
llm_stream = OpenAI(
    streaming=True,
    callbacks=[ChatCallbackHandler()],
    openai_api_key=OPENAI_API_KEY,
)

conn = get_sqlite_connection(csv_files)

questions = [item["question"] for item in EXAMPLES]
vectorstore_examples = get_vectorstore_examples(EXAMPLES, OPENAI_API_KEY)

tour_rag = SQLWorkflow(CHATLLM, llm_stream, conn, vectorstore_examples)
app = tour_rag.setup_workflow()

# UI 구성
st.title("반려동물 동반 시설 가이드")
st.write(
    "🌟반려동물 동반 시설  가이드 챗봇에 오신 것을 환영합니다! 궁금하신 정보를 질문해주세요."
)
st.write(
    "🌟예시 질문: 종로구 무악동에 있는 24시간 동물병원을 알려주세요. 부산 동구에 있는 주차 가능한 카페를 알려주세요. 인천에 있는 반려동물 동반 추가요금 없는 펜션 알려주세요."
)

paint_history()

# 사용자 입력 처리
message = st.chat_input("Ask anything about pet facilities...")

if message:
    send_message(message, "human")
    inputs = {"question": message}
    with st.chat_message("ai"):
        response = app.invoke(inputs)

button = st.sidebar.button("Show Workflow")
if button:
    with st.sidebar:
        st.image(app.get_graph().draw_mermaid_png(), caption="Sunrise by the mountains")
