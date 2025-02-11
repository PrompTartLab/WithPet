from uuid import UUID, uuid4
from datetime import datetime, timezone
import requests
import os
from typing import Optional, Dict, Any


class TracingManager:
    def __init__(self, api_key: str, project: str = "tour-guide-rag"):
        self.api_key = api_key
        self.project = project
        self.headers = {"x-api-key": api_key}
        self.current_workflow_run: Optional[UUID] = None
        self.current_node_run: Optional[UUID] = None

    def start_workflow_run(self, workflow_name: str, inputs: Dict[str, Any]) -> UUID:
        """워크플로우 실행을 시작합니다."""
        self.current_workflow_run = uuid4()
        self._post_run(
            self.current_workflow_run, f"{workflow_name} Workflow", "chain", inputs
        )
        return self.current_workflow_run

    def start_node_run(self, node_name: str, inputs: Dict[str, Any]) -> UUID:
        """노드 실행을 시작합니다."""
        if not self.current_workflow_run:
            raise ValueError("Workflow run must be started first")

        self.current_node_run = uuid4()
        self._post_run(
            self.current_node_run,
            f"Node: {node_name}",
            "llm",
            inputs,
            self.current_workflow_run,
        )
        return self.current_node_run

    def end_run(self, run_id: UUID, outputs: Dict[str, Any]) -> None:
        """실행을 종료합니다."""
        self._patch_run(run_id, outputs)
        if run_id == self.current_workflow_run:
            self.current_workflow_run = None
        elif run_id == self.current_node_run:
            self.current_node_run = None

    def _post_run(
        self,
        run_id: UUID,
        name: str,
        run_type: str,
        inputs: Dict[str, Any],
        parent_id: Optional[UUID] = None,
    ) -> None:
        data = {
            "id": run_id.hex,
            "name": name,
            "run_type": run_type,
            "inputs": inputs,
            "start_time": datetime.utcnow().isoformat(),
            "project": self.project,
        }
        if parent_id:
            data["parent_run_id"] = parent_id.hex

        requests.post(
            "https://api.smith.langchain.com/runs", json=data, headers=self.headers
        )

    def _patch_run(self, run_id: UUID, outputs: Dict[str, Any]) -> None:
        requests.patch(
            f"https://api.smith.langchain.com/runs/{run_id}",
            json={
                "outputs": outputs,
                "end_time": datetime.now(timezone.utc).isoformat(),
            },
            headers=self.headers,
        )
