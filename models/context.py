class Context:
    def __init__(self, llm, llm_stream, conn):
        self.llm = llm
        self.llm_stream = llm_stream
        self.conn = conn
