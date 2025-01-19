from langgraph.graph import END, StateGraph
from models.graph_state import GraphState
from models.context import Context
from nodes.select_data_source import SelectDataNode
from nodes.get_example import GetExampleNode
from nodes.generate_sql import GenerateSQLNode 
from nodes.verify_sql import VerifySQLNode
from nodes.perform_rag import PerformRAGNode
from nodes.retrieve_from_web import WebSearchNode
from nodes.execute_sql import ExecuteSQLNode
from nodes.generate_final_answer import GenerateAnswerNode, HandleNoDataNode, HandleNotRelevantNode
from nodes.routing import check_data_source, check_sql_status

class SQLWorkflow:
    """
    Tabular 데이터 기반 정보를 제공하기 위해 RAG(Retrieval-Augmented Generation) 로직을 구성한 클래스.
    주어진 LLM들을 통해 사용자의 질의에 맞는 데이터를 SQL을 통해 검색하고, 적절한 답변을 생성한다.
    내부적으로 SQLite를 사용하여 CSV 데이터를 관리한다.
    """

    def __init__(
        self, llm_chat, llm_stream, conn, vector_store_example
    ):
        """
        Args:
            llm_chat: 모델 function call(Structured LLM)을 활용할 수 있는 LLM (ex. ChatOpenAI)
            llm: 최종 답변 생성을 위한 LLM
        """
        self.llm_chat = llm_chat
        self.llm_stream = llm_stream
        self.workflow = StateGraph(GraphState)
        self.context = Context(
            llm_chat, llm_stream, conn, vector_store_example, None
        )
        self.app = None

    def setup_workflow(self):
        select_data_node = SelectDataNode(self.context)
        get_example_node = GetExampleNode(self.context)
        generate_sql_node = GenerateSQLNode(self.context)
        verify_sql_node = VerifySQLNode(self.context)
        web_search_node = WebSearchNode(self.context)
        generate_answer_node = GenerateAnswerNode(self.context)
        handle_no_data_node = HandleNoDataNode(self.context)
        handle_not_relevant_node = HandleNotRelevantNode(self.context)

        self.workflow.add_node("select_data_source", select_data_node.execute)
        self.workflow.add_node("get_example", get_example_node.execute)
        self.workflow.add_node("generate_sql", generate_sql_node.execute)
        self.workflow.add_node("verify_sql", verify_sql_node.execute)
        self.workflow.add_node("retrieve_from_web", web_search_node.execute)
        self.workflow.add_node("generate_final_answer", generate_answer_node.execute)
        self.workflow.add_node("handle_no_data", handle_no_data_node.execute)
        self.workflow.add_node("handle_not_relevant", handle_not_relevant_node.execute)

        self.workflow.add_edge("get_example", "generate_sql")
        self.workflow.add_edge("generate_sql", "verify_sql")
        self.workflow.add_edge("retrieve_from_web", "generate_final_answer")
        self.workflow.add_edge("generate_final_answer", END)
        self.workflow.add_edge("handle_no_data", END)

        self.workflow.add_conditional_edges(
            "select_data_source",
            check_data_source,
            {
                "pet_places": "get_example",
                "web": "retrieve_from_web",
                "not_relevant" : "handle_not_relevant"
            },
        )
        self.workflow.add_conditional_edges(
            "verify_sql",
            check_sql_status,
            {
                'retry': "generate_sql", 
                'data exists': "generate_final_answer",
                'no data': "handle_no_data",
            },
        )

        self.workflow.set_entry_point("select_data_source")
        self.app = self.workflow.compile()
        return self.app

class SQLRAGWorkflow:
    """
    Tabular 데이터 기반 정보를 제공하기 위해 RAG(Retrieval-Augmented Generation) 로직을 구성한 클래스.
    주어진 LLM들을 통해 사용자의 질의에 맞는 데이터를 SQL을 통해 검색하고, RAG 기반으로 추가로 데이터를 필터링한다.
    내부적으로 SQLite를 사용하여 CSV 데이터를 관리한다.
    """

    def __init__(
        self, llm_chat, llm_stream, conn, vector_store_example, vector_store_data
    ):
        """
        Args:
            llm_chat: 모델 function call(Structured LLM)을 활용할 수 있는 LLM (ex. ChatOpenAI)
            llm: 최종 답변 생성을 위한 LLM
        """
        self.llm_chat = llm_chat
        self.llm_stream = llm_stream
        self.workflow = StateGraph(GraphState)
        self.context = Context(
            llm_chat, llm_stream, conn, vector_store_example, vector_store_data
        )
        self.app = None

    def setup_workflow(self):
        select_data_node = SelectDataNode(self.context)
        get_example_node = GetExampleNode(self.context)
        generate_sql_node = GenerateSQLNode(self.context)
        execute_sql_node = ExecuteSQLNode(self.context)
        perform_rag_node = PerformRAGNode(self.context)
        web_search_node = WebSearchNode(self.context)
        generate_answer_node = GenerateAnswerNode(self.context)
        handle_no_data_node = HandleNoDataNode(self.context)

        # 노드 추가
        self.workflow.add_node("select_data_source", select_data_node.execute)
        self.workflow.add_node("get_example", get_example_node.execute)
        self.workflow.add_node("generate_sql", generate_sql_node.execute)
        self.workflow.add_node("execute_sql", execute_sql_node.execute)
        self.workflow.add_node("perform_rag", perform_rag_node.execute)
        self.workflow.add_node("retrieve_from_web", web_search_node.execute)
        self.workflow.add_node("generate_final_answer", generate_answer_node.execute)
        self.workflow.add_node("handle_no_data", handle_no_data_node.execute)

        self.workflow.add_edge("get_example", "generate_sql")
        self.workflow.add_edge("generate_sql", "execute_sql")
        self.workflow.add_edge("perform_rag", "generate_final_answer")
        self.workflow.add_edge("retrieve_from_web", "generate_final_answer")
        self.workflow.add_edge("generate_final_answer", END)
        self.workflow.add_edge("handle_no_data", END)

        self.workflow.add_conditional_edges(
            "select_data_source",
            check_data_source,
            {
                "tourist_spots": "get_example",
                "restaurants": "get_example",
                "web": "retrieve_from_web",
            },
        )

        self.workflow.add_conditional_edges(
            "execute_sql",
            check_sql_status,
            {
                "retry": "generate_sql",
                "data over 10": "perform_rag",
                "generation error": "perform_rag",
                "data under 10": "generate_final_answer",
                "no data": "handle_no_data",
            },
        )

        self.workflow.set_entry_point("select_data_source")
        self.app = self.workflow.compile()
        return self.app
