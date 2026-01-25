# workflow/state.py
from typing import TypedDict, Optional, Any, List


class GraphState(TypedDict):
    # user input
    query: str

    # optional inputs
    image_path: Optional[str]        # for vision flow
    dataframe_path: Optional[str]    # csv / parquet

    # routing
    decision: Optional[str]          # simple | vision | sql

    # intermediate results
    vision_result: Optional[str]
    sql_query: Optional[str]
    sql_result: Optional[Any]

    # final answer
    final_answer: Optional[str]
