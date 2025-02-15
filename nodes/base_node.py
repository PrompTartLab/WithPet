class BaseNode:
    def __init__(self, context):
        self.context = context  # Shared context for LLM, DB connection, etc.

    def execute(self, state):
        raise NotImplementedError("Subclasses must implement the 'execute' method.")
