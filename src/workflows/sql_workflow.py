from typing import Dict, List

from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph

from ..modules.graph_state import GraphState
from ..modules.context import Context

from ..nodes.select_data_source import SelectDataNode
from ..nodes.get_example import GetExampleNode
from ..nodes.generate_sql import GenerateSQLNode
from ..nodes.execute_sql import ExecuteSQLNode
from ..nodes.perform_rag import PerformRAGNode
from ..nodes.generate_final_answer import (
    GenerateAnswerNode,
    HandleNoDataNode,
    HandleNotRelevantNode,
)


class SQLWorkflow:
    """
    Tabular 데이터 기반 정보를 제공하기 위해 RAG(Retrieval-Augmented Generation) 로직을 구성한 클래스.
    주어진 LLM들을 통해 사용자의 질의에 맞는 데이터를 SQL을 통해 검색하고, 적절한 답변을 생성한다.
    내부적으로 SQLite를 사용하여 CSV 데이터를 관리한다.
    """

    def __init__(
        self,
        context: Context,
        source_routing_template: PromptTemplate,
        schemas: Dict[str, str],
        sql_generation_template: PromptTemplate,
        source_columns: Dict[str, List[str]],
        answer_generation_template: PromptTemplate,
    ) -> None:
        """
        Args:
            llm_chat: 모델 function call(Structured LLM)을 활용할 수 있는 LLM (ex. ChatOpenAI)
            llm_stream: 최종 답변 생성을 위한 LLM
        """
        self.workflow = StateGraph(GraphState)
        self.app = None
        self.context = context
        self.source_routing_template = source_routing_template
        self.schemas = schemas
        self.sql_generation_template = sql_generation_template
        self.source_columns = source_columns
        self.answer_generation_template = answer_generation_template

    def setup_workflow(self) -> CompiledStateGraph:
        select_data_node = SelectDataNode(
            context=self.context,
            schemas=self.schemas,
            source_routing_template=self.source_routing_template,
        )
        get_example_node = GetExampleNode(context=self.context)
        generate_sql_node = GenerateSQLNode(
            context=self.context,
            sql_generation_template=self.sql_generation_template,
        )
        execute_sql_node = ExecuteSQLNode(
            context=self.context,
            source_columns=self.source_columns,
        )
        perform_rag_node = PerformRAGNode(
            context=self.context,
        )
        generate_answer_node = GenerateAnswerNode(
            context=self.context,
            answer_generation_template=self.answer_generation_template,
        )
        handle_no_data_node = HandleNoDataNode(context=self.context)
        handle_not_relevant_node = HandleNotRelevantNode(context=self.context)

        self.workflow.add_node(
            "select_data_source",
            select_data_node.execute,
        )
        self.workflow.add_node(
            "get_example",
            get_example_node.execute,
        )
        self.workflow.add_node(
            "generate_sql",
            generate_sql_node.execute,
        )
        self.workflow.add_node(
            "execute_sql",
            execute_sql_node.execute,
        )
        self.workflow.add_node(
            "perform_rag",
            perform_rag_node.execute,
        )
        self.workflow.add_node(
            "generate_final_answer",
            generate_answer_node.execute,
        )
        self.workflow.add_node(
            "handle_no_data",
            handle_no_data_node.execute,
        )
        self.workflow.add_node(
            "handle_not_relevant",
            handle_not_relevant_node.execute,
        )

        self.workflow.add_edge(
            "get_example",
            "generate_sql",
        )
        self.workflow.add_edge(
            "generate_sql",
            "execute_sql",
        )
        self.workflow.add_edge(
            "perform_rag",
            "generate_final_answer",
        )
        self.workflow.add_edge(
            "generate_final_answer",
            END,
        )
        self.workflow.add_edge(
            "handle_no_data",
            END,
        )

        self.workflow.add_conditional_edges(
            "select_data_source",
            self.check_data_source,
            {
                "PET_PLACES": "get_example",
                "NOT_RELEVANT": "handle_not_relevant",
            },
        )
        self.workflow.add_conditional_edges(
            "execute_sql",
            self.check_sql_status,
            {
                "RETRY": "generate_sql",
                "DATA_EXISTS": "perform_rag",
                "NO_DATA": "handle_no_data",
            },
        )

        self.workflow.set_entry_point("select_data_source")
        self.app = self.workflow.compile()
        return self.app

    def check_data_source(
        self,
        state: GraphState,
    ) -> GraphState:
        return state["data_source"]

    def check_sql_status(
        self,
        state: GraphState,
    ) -> GraphState:
        return state["sql_status"]
