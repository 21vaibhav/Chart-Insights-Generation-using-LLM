# workflow/graph_builder.py
from langgraph.graph import StateGraph, END
from workflow.state import GraphState
from workflow.router import router_node
from workflow.vision_flow import vision_node, vision_interpret_node
from workflow.sql_flow import (
    sql_generate_node,
    sql_execute_node,
    sql_interpret_node,
)
# from llm.models.qwen_client import QwenClient
from llm.models.sqlcoder_client import SQLCoderClient

# qwen = QwenClient()
sqlc = SQLCoderClient()


def build_graph(central_llm, sqlc):
    graph = StateGraph(GraphState)

    # nodes
    sql_graph.add_node(
    "sql_router",
    router_node(
        llm=mistral_llm,
        router_prompt=SQL_ROUTER_PROMPT,
        valid_routes={"answer_directly", "generate_sql"},
    ),
    )

    # graph.add_node("vision", vision_node(qwen))
    # graph.add_node("vision_interpret", vision_interpret_node(central_llm))

    graph.add_node("sql_generate", sql_generate_node(sqlc))
    graph.add_node("sql_execute", sql_execute_node(sqlc))
    graph.add_node("sql_interpret", sql_interpret_node(central_llm))

    # entry
    graph.set_entry_point("sql_router")

    # conditional routing
    graph.add_conditional_edges(
        "sql_router",
        lambda state: state["route"],
        {
            "answer_directly": "answer_directly",
            "generate_sql": "sql_generate",
        },
    )

    # vision flow
    # graph.add_edge("vision", "vision_interpret")
    # graph.add_edge("vision_interpret", END)

    # sql flow
    graph.add_edge("sql_generate", "sql_execute")
    graph.add_edge("sql_execute", "sql_interpret")
    graph.add_edge("sql_interpret", END)
    sql_graph.add_edge("answer_directly", END)


    return graph.compile()
