# workflow/sql_flow.py
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate



INTERPRET_PROMPT = ChatPromptTemplate.from_template(
    """
You are a maritime analyst.

Given the SQL result below, answer the user query clearly with numbers.

STRICT RULES:
- Use domain knowledge ONLY to interpret the SQL result
- Do NOT restate the question
if SQL result is none/invalid, then display "cant generate response for your query. Try some other query". 

SQL result:
{sql_result}

RELEVANT DOMAIN KNOWLEDGE:
{rag_context}

User query:
{query}
"""
)


def sql_generate_execute_node(sqlcoder):
    def _generate_execute(state):
        
        sqlcoder.bind_dataframe(df = state["dataframe"],table_name = state['table_name'])
        response = sqlcoder.get_result(state['query'])

        if isinstance(response, dict):
            return {
            "sql_query": response['sql'],
            "sql_result": response['data']
            }
        
        print(f"\n[System]: {response}")
        return {
        "sql_query": None,
        "sql_result": None
        }

    return _generate_execute


def sql_interpret_node(ossgpt, retriever):

    def _interpret(state):

        rag_context = retriever.invoke(state['query'])

        prompt = INTERPRET_PROMPT.format(
            sql_result = state['sql_result'],
            query=state["query"], 
            rag_context = rag_context
        )

        response = ossgpt.generate(
            prompt=prompt
        )

        return {"final_answer": response}

    return _interpret
