import streamlit as st
import os
import time

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from models.llm import CHATLLM
from workflows.sql_workflow import SQLWorkflow
from configs.examples import EXAMPLES
from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain_core.tracers import LangChainTracer
from langchain.callbacks.manager import CallbackManager


# OpenAI API 키 로드
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Langsmith tracing을 위한 키 로드
LANGCHAIN_API_KEY = st.secrets["LANGCHAIN_API_KEY"]
LANGCHAIN_PROJECT = st.secrets["LANGCHAIN_PROJECT"]
LANGCHAIN_TRACING_V2 = "true"
LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"


# 메시지 세션 스테이트 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.set_page_config(page_title="반려동물 시설 가이드", page_icon="🐕")


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


def send_message(message: str, role: str, save: bool = True, placeholder=None) -> None:
    """
    채팅 UI에 메시지를 출력합니다.
    save=True인 경우, 세션 스테이트에도 메시지를 저장합니다.
    placeholder가 제공되면 UI 메시지를 그 안에서 업데이트합니다.
    """
    if placeholder:
        placeholder.markdown(
            message
        )  # Update existing message if placeholder is provided
    else:
        with st.chat_message(role):
            st.markdown(message)  # Normal UI message if no placeholder

    if save:
        save_message(message, role)


def paint_history() -> None:
    """세션 스테이트에 기록된 메시지를 모두 다시 출력합니다."""
    for msg in st.session_state["messages"]:
        send_message(msg["message"], msg["role"], save=False)


@st.cache_resource
def get_embeddings(api_key):
    return OpenAIEmbeddings(openai_api_key=api_key)


tracer = LangChainTracer(project_name=LANGCHAIN_PROJECT)
callback_manager = CallbackManager([tracer])

chat_callback_handler = ChatCallbackHandler()

llm_stream = ChatOpenAI(
    model="gpt-4o",
    streaming=True,
    callbacks=[chat_callback_handler],
    openai_api_key=OPENAI_API_KEY,
)
vectorstore_examples = FAISS.load_local(
    "faiss_example",
    get_embeddings(OPENAI_API_KEY),
    allow_dangerous_deserialization=True,
)
tour_rag = SQLWorkflow(CHATLLM, llm_stream, vectorstore_examples)
app = tour_rag.setup_workflow()


st.markdown(
    """
    <h2 style='text-align: center; color: #FF914D;'>
        🐾 반려동물 동반 시설 가이드 🐾
    </h2>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p style="text-align: center; font-size: 18px; color: #555; font-weight: bold;">
        반려동물과 함께 할 수 있는 장소를 찾아보세요! 🐶🐱
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="
        background-color: #FFF3E6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    ">
        <h5 style="color: #FF6B00;">💡 이용 가능한 질문 예시</h5>
        <ul style="font-size: 16px; color: #333;">
            <li>🏥 <b>강남구 신사동</b>에 <b>일요일</b>에도 영업하는 동물병원</b>이 있나요?</li>
            <li>☕ <b>부산 동구</b>에 <b>주차 가능한</b> <b>카페</b> 알려줘.</li>
            <li>🏡 <b>인천</b>에 있는 <b>반려동물 추가 요금 없는 펜션</b>을 찾아주세요.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div>
        <p style="font-size: 14px; color: #666; text-align: center; margin-top: 15px;">
            <i>※ 해당 챗봇이 제공하는 모든 시설은 반려동물 동반 가능 시설입니다.</i>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("<br><br>", unsafe_allow_html=True)


# Initialize session state for user selections
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "카페"

# Initialize session state list for selected options
if "selected_options" not in st.session_state:
    st.session_state.selected_options = []

# Sidebar Design
with st.sidebar:

    # Use `st.form` to prevent auto-rerun for filters
    with st.form("filter_form"):
        st.markdown("### 📍 지역을 선택하세요")
        city = st.selectbox(
            "지역 선택",
            ["서울", "부산", "인천", "대구", "대전", "광주", "울산", "세종", "제주"],
            label_visibility="collapsed",
        )
        st.markdown("### 🏠 시설 유형")
        category = st.radio(
            "시설 유형",  # Empty label to remove space
            [
                "☕ 카페",
                "🏡 펜션",
                "🏨 호텔",
                "🏥 동물병원",
                "💊 동물약국",
                "✂️ 미용",
                "🛒 반려동물용품",
                "🏢 위탁관리",
            ],
            index=[
                "카페",
                "펜션",
                "호텔",
                "동물병원",
                "동물약국",
                "미용",
                "반려동물용품",
                "위탁관리",
            ].index(st.session_state.selected_category),
            label_visibility="collapsed",
        )

        checkbox_options = {
            "🚗 주차 가능": "주차 가능",
            "🗓️ 주말 운영": "주말 운영",
            "⏰ 24시간 운영": "24시간 운영",
            "🪙 반려동물 추가 요금 없음": "반려동물 추가 요금 없음",
            "🐈 반려동물 크기 제한 없음": "반려동물 크기 제한 없음",
        }
        st.markdown("### 🔍 추가 옵션")
        selected_values = set(st.session_state.selected_options)
        for label, key in checkbox_options.items():
            if st.checkbox(label, value=key in selected_values):
                selected_values.add(key)  # Add selected option
            else:
                selected_values.discard(key)  # Remove unselected option

        submitted = st.form_submit_button("🔎 검색하기")

        if submitted:
            st.session_state.selected_category = category.split()[1]
            st.session_state.selected_options = list(selected_values)

            query_text = f"{city} 지역의 {st.session_state.selected_category}{' ('+ ', '.join(st.session_state.selected_options)+ ')' if st.session_state.selected_options else ''}"

            # 검색 버튼
            st.markdown("<br>", unsafe_allow_html=True)
            st.session_state.inputs = {"question": query_text}
            st.session_state.trigger_search = True  # Flag to trigger app invoke

paint_history()

# Chat Input
message = st.chat_input("반려동물 동반 시설에 대해 질문해 주세요...")

if message:
    st.session_state.inputs = {"question": message}
    st.session_state.trigger_search = True  # Flag to trigger app invoke

# Process the request if search was triggered
if st.session_state.get("trigger_search", False):
    send_message(st.session_state.inputs["question"], "human")

    with st.chat_message("ai"):
        placeholder = st.empty()
        placeholder.markdown(
            "⌛질문에 해당하는 장소를 찾고 있습니다... 잠시만 기다려주세요."
        )

    response = app.invoke(st.session_state.inputs)
    print(response["answer"])

    if response["data_source"] == "not_relevant" or response["sql_status"] == "no data":
        send_message(response["answer"], "ai", placeholder)

    # Reset trigger after processing
    st.session_state.trigger_search = False
    st.rerun()
