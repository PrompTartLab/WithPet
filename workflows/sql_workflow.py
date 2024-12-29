from langgraph.graph import END, StateGraph
from models.graph_state import GraphState
from models.context import Context
from nodes.select_data_source import SelectDataNode
from nodes.generate_sql import GenerateSQLNode
from nodes.retrieve_from_web import WebSearchNode
from nodes.verify_sql import VerifySQLNode
from nodes.generate_final_answer import GenerateAnswerNode, HandleNoDataNode
from nodes.routing import get_data_source, get_sql_status


class SQLWorkflow:
    """
    부산 관광 정보를 제공하기 위해 RAG(Retrieval-Augmented Generation) 로직을 구성한 클래스.
    주어진 LLM들을 통해 사용자의 질의에 맞는 데이터를 검색하고, 적절한 답변을 생성한다.
    내부적으로 SQLite를 사용하여 CSV 데이터를 관리한다.
    """

    def __init__(self, llm_chat, llm_stream, conn):
        """
        Args:
            llm_chat: 모델 function call(Structured LLM)을 활용할 수 있는 LLM (ex. ChatOpenAI)
            llm: 최종 답변 생성을 위한 LLM
        """
        self.llm_chat = llm_chat
        self.llm_stream = llm_stream
        self.workflow = StateGraph(GraphState)
        self.context = Context(llm_chat, llm_stream, conn)
        self.app = None

        self._setup_workflow()

    def _setup_workflow(self):
        select_data_node = SelectDataNode(self.context)
        generate_sql_node = GenerateSQLNode(self.context)
        verify_sql_node = VerifySQLNode(self.context)
        web_search_node = WebSearchNode(self.context)
        generate_answer_node = GenerateAnswerNode(self.context)
        handle_no_data_node = HandleNoDataNode(self.context)

        # 노드 추가
        self.workflow.add_node("select_data_source", select_data_node.execute)
        self.workflow.add_node("generate_sql", generate_sql_node.execute)
        self.workflow.add_node("retrieve_from_web", web_search_node.execute)
        self.workflow.add_node("verify_sql", verify_sql_node.execute)
        self.workflow.add_node("generate_final_answer", generate_answer_node.execute)
        self.workflow.add_node("handle_no_data", handle_no_data_node.execute)

        # 각 노드의 실행이 끝나면 종료(END)로 가는 엣지
        self.workflow.add_edge("generate_sql", "verify_sql")
        self.workflow.add_edge("retrieve_from_web", "generate_final_answer")
        self.workflow.add_edge("generate_final_answer", END)
        self.workflow.add_edge("handle_no_data", END)

        # 분기 조건(conditional edges)
        self.workflow.add_conditional_edges(
            "select_data_source",
            get_data_source,
            {
                "local_tourist_spots": "generate_sql",
                "foreign_tourist_spots": "generate_sql",
                "restaurants": "generate_sql",
                "web": "retrieve_from_web",
            },
        )

        self.workflow.add_conditional_edges(
            "verify_sql",
            get_sql_status,
            {
                "retry": "generate_sql",
                "data exists": "generate_final_answer",
                "no data": "handle_no_data",
            },
        )
        # Set entry point
        self.workflow.set_entry_point("select_data_source")
        self.app = self.workflow.compile()
