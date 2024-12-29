from models.graph_state import GraphState


def get_data_source(state: GraphState) -> GraphState:
    return state["data_source"]


def get_sql_status(state: GraphState) -> GraphState:
    return state["sql_status"]
