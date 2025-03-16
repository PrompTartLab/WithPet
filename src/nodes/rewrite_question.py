from typing import Dict

from langchain_core.prompts import PromptTemplate

from .base_node import BaseNode

from ..modules.context import Context
from ..modules.graph_state import GraphState
from ..modules.response_schema import RefinedQuestion


class RewriteQuestionNode(BaseNode):
    def __init__(
        self,
        context: Context,
        question_refinement_template: PromptTemplate,
    ) -> None:
        super().__init__(context=context)
        self.question_refinement_template = question_refinement_template

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        llm = self.context.llm
        question = state["question"]
        generated_sql = state["generated_sql"]

        structured_llm = llm.with_structured_output(RefinedQuestion)
        router = self.question_refinement_template | structured_llm
        response = router.invoke(
            {
                "question": question,
                "generated_sql": generated_sql,
            }
        )
        return GraphState(refined_question=response.question)
