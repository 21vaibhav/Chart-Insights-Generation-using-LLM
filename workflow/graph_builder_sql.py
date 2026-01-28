# workflow/graph_builder.py
from langgraph.graph import StateGraph, END
from .state import GraphState
from .router import router_node, SQL_ROUTER_PROMPT
# from workflow.vision_flow import vision_node, vision_interpret_node
from .sql_flow import (
    sql_generate_execute_node,
    sql_interpret_node,
)
# from llm.models.qwen_client import QwenClient
# from llm.models.sqlcoder_client import SQLQueryManager
# qwen = QwenClient()
# sqlc = SQLCoderClient()


def build_graph_sql(ossgpt, sqlc, retriever):
    graph = StateGraph(GraphState)

    # nodes
    graph.add_node(
    "sql_router",
    router_node(
        llm=ossgpt,
        router_prompt=SQL_ROUTER_PROMPT,
        valid_routes={"answer_directly", "generate_sql"},
        retriever=retriever
    ),
    )

    # graph.add_node("vision", vision_node(qwen))
    # graph.add_node("vision_interpret", vision_interpret_node(central_llm))

    graph.add_node("sql_generate_execute", sql_generate_execute_node(sqlc))
    graph.add_node("sql_interpret", sql_interpret_node(ossgpt,retriever))

    # entry
    graph.set_entry_point("sql_router")

    # conditional routing
    graph.add_conditional_edges(
        "sql_router",
        lambda state: state["decision"],
        {
            "answer_directly": END,
            "generate_sql": "sql_generate_execute",
        },
    )

    # vision flow
    # graph.add_edge("vision", "vision_interpret")
    # graph.add_edge("vision_interpret", END)

    # sql flow
    graph.add_edge("sql_generate_execute", "sql_interpret")
    graph.add_edge("sql_interpret", END)


    return graph.compile()
