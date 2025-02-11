from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class BaseNode:
    def __init__(self, context, tracer=None):
        self.context = context
        self.tracer = tracer
        self.node_name = self.__class__.__name__

    def _get_model_params(self) -> Dict[str, Any]:
        """Get model parameters for tracing"""
        try:
            llm = self.context.llm
            return {
                "model": llm.model_name,
                "temperature": llm.temperature,
                "model_kwargs": (
                    llm.model_kwargs if hasattr(llm, "model_kwargs") else {}
                ),
            }
        except Exception as e:
            logger.warning(f"Failed to get model parameters: {str(e)}")
            return {}

    def _trace_node(self, inputs: Dict[str, Any], prompt_template: str = None):
        """Start node tracing with common parameters"""
        if not self.tracer:
            return None

        try:
            trace_inputs = {**inputs, **self._get_model_params()}
            if prompt_template:
                # PromptTemplate 객체를 문자열로 변환
                if hasattr(prompt_template, "template"):
                    trace_inputs["prompt_template"] = prompt_template.template
                else:
                    trace_inputs["prompt_template"] = str(prompt_template)

            return self.tracer.start_node_run(self.node_name, trace_inputs)
        except Exception as e:
            logger.warning(f"Failed to start node tracing: {str(e)}")
            return None

    def _end_trace(self, node_run_id, outputs: Dict[str, Any], status: str = "success"):
        """End node tracing with outputs and status"""
        if not self.tracer or not node_run_id:
            return

        try:
            self.tracer.end_run(node_run_id, {**outputs, "status": status})
        except Exception as e:
            logger.warning(f"Failed to end node tracing: {str(e)}")

    def execute(self, state):
        """Abstract method that must be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement the 'execute' method.")
