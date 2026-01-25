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
from llm.models.qwen_client import QwenClient
# from llm.models.sqlcoder_client import SQLCoderClient

qwen = QwenClient()
# sqlc = SQLCoderClient()


def build_graph(central_llm, sqlc):
    vision_graph = StateGraph(GraphState)

    # nodes
    vision_graph.add_node(
        "vision_router",
        router_node(
            llm=mistral_llm,
            router_prompt=VISION_ROUTER_PROMPT,
            valid_routes={"answer_directly", "extract_from_image"},
        ),
    )

    vision_graph.add_node("vision", vision_node(qwen))

    vision_graph.add_node("vision_interpret", vision_interpret_node(central_llm))

    # graph.add_node("sql_generate", sql_generate_node(sqlc))
    # graph.add_node("sql_execute", sql_execute_node(sqlc))
    # graph.add_node("sql_interpret", sql_interpret_node(central_llm))

    # entry
    vision_graph.set_entry_point("vision_router")

    # conditional routing
    vision_graph.add_conditional_edges(
        "vision_router",
        lambda state: state["route"],
        {
            "answer_directly": "answer_directly",
            "extract_from_image": "vision_extract",
            # "sql": "sql_generate",
        },
    )

    # vision flow
    vision_graph.add_edge("vision_extract", "vision_interpret")
    vision_graph.add_edge("vision_interpret", END)
    vision_graph.add_edge("answer_directly", END)

    # sql flow
    # graph.add_edge("sql_generate", "sql_execute")
    # graph.add_edge("sql_execute", "sql_interpret")
    # graph.add_edge("sql_interpret", END)

    return vision_graph.compile()
