# pipelines/graph_pipeline.py

import streamlit as st
from llm.models.llamav_client import LlamavClient
from llm.models.oss_gpt_client import OssGptClient
from llm.models.sqlcoder_client import SQLQueryManager
from workflow.graph_builder_vision import build_graph_vision
from workflow.graph_builder_sql import build_graph_sql
from .rag_pipeline import build_knowledge_base


class ModelLoad:
    def __init__(self):
        # Load ONCE
        self.ossgpt = OssGptClient()
        self.llamav = LlamavClient()
        self.sqlcoder = SQLQueryManager()
        self.retriever = build_knowledge_base(json_path=r"C:\Users\Dell\OneDrive\Desktop\project_2026\Chart-Insights-Generation-using-LLM\knowledge_base\Relations.json",md_path=r"C:\Users\Dell\OneDrive\Desktop\project_2026\Chart-Insights-Generation-using-LLM\knowledge_base\Concepts.md")
        

        # Build graph ONCE
        self.graph_vision = build_graph_vision(
            ossgpt=self.ossgpt,
            llamav=self.llamav,
            retriever = self.retriever
        )

        self.graph_sql = build_graph_sql(
            ossgpt = self.ossgpt,
            sqlc = self.sqlcoder,
            retriever = self.retriever
        )

    ## -----------------Vision_pipe-------------------
    def graph_vision_pipe(self, image, user_query):
        result = self.graph_vision.invoke({
            "query": user_query,
            "image": image
        })
        return result.get("vision_result"), result.get("final_answer")
    
    ##------------------SQL_pipe-----------------------
    def graph_sql_pipe(self, dataframe, user_query,table_name) :
        result = self.graph_sql.invoke({
            "query": user_query,
            "dataframe": dataframe,
            "table_name":table_name
        })

        return result.get("sql_result"), result.get("final_answer"),result.get('sql_query')


@st.cache_resource(show_spinner="Loading LLMs...")
def get_model():
    return ModelLoad()
