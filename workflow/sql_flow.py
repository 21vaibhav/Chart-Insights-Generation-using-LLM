# workflow/sql_flow.py
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate


# - Table name is `data` in rules or not 

SQL_PROMPT = ChatPromptTemplate.from_template(
    """
You are an expert SQL generator.

Given the table schema below, generate a valid SQL query.

Rules:
- Use ONLY columns present in the schema
- Do NOT hallucinate columns
- Do NOT add explanations


Schema:
{schema}

User query:
{query}

Return ONLY SQL.
"""
)


INTERPRET_PROMPT = ChatPromptTemplate.from_template(
    """
You are a maritime analyst.

Given the SQL result below, answer the user query clearly with numbers.

SQL result:
{sql_result}

User query:
{query}
"""
)


def sql_generate_node(sqlcoder):
    def _generate(state):
        df = pd.read_csv(state["dataframe_path"])

        def pandas_to_sqlite(dtype):
            if "int" in str(dtype):
                return "INTEGER"
            if "float" in str(dtype):
                return "REAL"
            return "TEXT"

        schema = "\n".join(
        f"{c} {pandas_to_sqlite(t)}"
        for c, t in df.dtypes.items()
        )

        prompt = SQL_PROMPT.invoke(
            {
                "schema": schema,
                "query": state["query"],
            }
        ).to_string()

        sql = sqlcoder.generate_sql(prompt)
        return {"sql_query": sql}

    return _generate


def sql_execute_node(sqlcoder):
    def _execute(state):
        df = pd.read_csv(state["dataframe_path"])
        result = sqlcoder.execute_sql(df, state["sql_query"])
        return {"sql_result": result}

    return _execute


def sql_interpret_node(central_llm):
    chain = INTERPRET_PROMPT | central_llm

    def _interpret(state):
        response = chain.invoke(
            {
                "sql_result": state["sql_result"].to_string(),
                "query": state["query"],
            }
        )
        return {"final_answer": response.content}

    return _interpret
