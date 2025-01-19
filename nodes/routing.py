from models.graph_state import GraphState


def check_data_source(state: GraphState) -> GraphState:
    return state["data_source"]


def check_sql_status(state: GraphState) -> GraphState:
    return state["sql_status"]
