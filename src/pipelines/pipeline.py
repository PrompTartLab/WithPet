import os

import streamlit as st

from langchain.callbacks.base import BaseCallbackHandler
from langgraph.graph.state import CompiledStateGraph
from langchain_openai import OpenAIEmbeddings

from hydra.utils import instantiate
from omegaconf import DictConfig

from ..utils.setup import SetUp
from ..workflows.sql_workflow import SQLWorkflow


OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

st.set_page_config(
    page_title="WithPet",
    page_icon="🐕",
)


class ChatCallbackHandler(BaseCallbackHandler):
    """
    LLM이 토큰 단위로 출력할 때마다 Streamlit UI에 실시간 업데이트해주는 콜백 핸들러입니다.
    """

    message = ""

    def on_llm_start(
        self,
        *args,
        **kwargs,
    ) -> None:
        """LLM이 시작될 때 호출됩니다. 토큰 누적용 빈 컨테이너를 만듭니다."""
        self.message_box = st.empty()

    def on_llm_end(
        self,
        *args,
        **kwargs,
    ) -> None:
        """LLM이 종료될 때 호출됩니다. 최종 메시지를 저장합니다."""
        save_message(
            self.message,
            "ai",
        )

    def on_llm_new_token(
        self,
        token,
        *args,
        **kwargs,
    ) -> None:
        """LLM이 새 토큰을 생성할 때마다 호출됩니다. 토큰을 누적해 UI에 표시합니다."""
        self.message += token
        self.message_box.markdown(self.message)


def save_message(
    message: str,
    role: str,
) -> None:
    """메시지를 세션 스테이트에 저장합니다."""
    st.session_state["messages"].append(
        {
            "message": message,
            "role": role,
        }
    )


def send_message(
    message: str,
    role: str,
    save: bool = True,
    placeholder=None,
) -> None:
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
        save_message(
            message,
            role,
        )


def paint_history() -> None:
    """세션 스테이트에 기록된 메시지를 모두 다시 출력합니다."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    for msg in st.session_state["messages"]:
        send_message(
            msg["message"],
            msg["role"],
            save=False,
        )


@st.cache_resource
def get_embeddings(api_key: str) -> OpenAIEmbeddings:
    return OpenAIEmbeddings(openai_api_key=api_key)


def load_workflow(
    config: DictConfig,
    stream: bool = True,
) -> CompiledStateGraph:

    chat_callback_handler = ChatCallbackHandler()
    embeddings = get_embeddings(api_key=config.openai_api_key)

    setup = SetUp(config)

    llm = setup.get_llm()
    llm_stream = setup.get_llm_stream(chat_callback_handler) if stream else llm
    conn = setup.get_connection()
    vs_example = setup.get_vs_example(embeddings=embeddings)
    if os.path.exists(config.vector_store_data):
        vs_data = setup.get_vs_data(embeddings=embeddings)
    else:
        vs_data = None

    context = setup.get_context(
        llm=llm,
        llm_stream=llm_stream,
        conn=conn,
        vs_example=vs_example,
        vs_data=vs_data,
    )

    source_routing_template = setup.get_prompt_template(
        prompt_type=config.prompt_type.source_routing_template
    )
    sql_generation_template = setup.get_prompt_template(
        prompt_type=config.prompt_type.sql_generation_template
    )
    source_columns = setup.get_source_columns()
    answer_generation_template = setup.get_prompt_template(
        prompt_type=config.prompt_type.answer_generation_template
    )

    workflow = SQLWorkflow(
        context=context,
        source_routing_template=source_routing_template,
        schemas=config.schemas,
        sql_generation_template=sql_generation_template,
        source_columns=source_columns,
        answer_generation_template=answer_generation_template,
    )

    app = workflow.setup_workflow()
    return app


def pipeline(
    config: DictConfig,
) -> None:

    app = load_workflow(
        config=config,
        stream=True,
    )

    st.markdown(
        """
        <h2 style='text-align: center; color: #FF914D;'>
            🐾 WithPet: 반려동물 동반 시설 가이드 🐾
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
                <li>🏥 <b>강남구 신사동</b>에 <b>일요일 오후 1시에</b> 영업하는 <b>동물병원</b>이 있나요?</li>
                <li>☕ <b>부산 동구</b>에 <b>주차 가능</b>한 <b>카페</b>를 알려주세요.</li>
                <li>🏡 <b>인천</b>에 있는 <b>반려동물 추가 요금 없는 펜션</b> 찾아줘.</li>
                <li>✂️ <b>종로구</b>에서 <b>저녁 7시</b>에 <b>미용</b> 가능한 곳</li>
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
        <br>
        """,
        unsafe_allow_html=True,
    )

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
            st.markdown(
                """
                <h1 style="display: flex; justify-content: left; align-items: center;">
                    🚀 Quick Search 
                    <span style="font-size: 12px; vertical-align: sub; margin-left: 8px; cursor: pointer;" 
                        title="지역과 시설 유형을 선택한 후 검색하기를 클릭하세요.">
                        ℹ️
                    </span>
                </h1>
                <br>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("### 📍 지역")
            city = st.selectbox(
                "지역 선택",
                [
                    "서울",
                    "부산",
                    "인천",
                    "대구",
                    "대전",
                    "광주",
                    "울산",
                    "세종",
                    "제주",
                ],
                label_visibility="collapsed",
            )
            st.markdown("### 🏠 시설 유형")
            category = st.radio(
                "시설 유형",  # Empty label to remove space
                [
                    "☕ 카페",
                    "🏡 펜션",
                    "🏥 동물병원",
                    "💊 동물약국",
                    "✂️ 미용",
                    "🛒 반려동물용품",
                    "🏢 위탁관리",
                ],
                index=[
                    "카페",
                    "펜션",
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
                "⛅ 아침 9시 이전 영업": "아침 9시 이전 영업",
                "🌙 밤 10시 이후 영업": "밤 10시 이후 영업",
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

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🔎 검색하기")

            if submitted:
                st.session_state.selected_category = category.split()[1]
                st.session_state.selected_options = list(selected_values)

                category = st.session_state.selected_category
                options = st.session_state.selected_options
                options_text = f" ({', '.join(options)})" if options else ""

                query_text = f"{city} 지역의 {category}{options_text}"

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
        send_message(
            st.session_state.inputs["question"],
            "human",
        )

        with st.chat_message("ai"):
            placeholder = st.empty()
            placeholder.markdown(
                "⌛질문에 해당하는 장소를 찾고 있습니다... 잠시만 기다려주세요."
            )

        response = app.invoke(st.session_state.inputs)

        if (
            response["data_source"] == "not_relevant"
            or response["sql_status"] == "no data"
        ):
            send_message(
                response["answer"],
                "ai",
                placeholder,
            )

        # Reset trigger after processing
        st.session_state.trigger_search = False
        st.rerun()
