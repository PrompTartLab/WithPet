class Context:
    def __init__(self, llm, llm_stream, conn, vs_example, vs_data):
        self.llm = llm
        self.llm_stream = llm_stream
        self.conn = conn
        self.vs_example = vs_example
        self.vs_data = vs_data
