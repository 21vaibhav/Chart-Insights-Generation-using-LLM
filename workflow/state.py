# workflow/state.py
from typing import TypedDict, Optional, Any, List


class GraphState(TypedDict):
    # user input
    query: str

    # optional inputs
    image: Optional[Any]        # for vision flow
    dataframe: Optional[Any]    # csv / parquet
    table_name: Optional[str]

    # routing
    decision: Optional[str]          

    # intermediate results
    vision_result: Optional[str]
    sql_query: Optional[str]
    sql_result: Optional[Any]

    # final answer
    final_answer: Optional[str]

