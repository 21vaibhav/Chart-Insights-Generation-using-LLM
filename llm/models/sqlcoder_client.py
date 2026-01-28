import pandas as pd
import duckdb
import re
import torch
import sqlglot  # New dependency
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from ..sqlcoder.sqlcoder_loader import generate_sql

class SQLQueryManager:
    def __init__(self, max_history=3):
        # self.table_name = table_name
        # self.con = duckdb.connect(database=":memory:")
        # self.con.register(table_name, df)
        self.history = []
        self.max_history = max_history
        # self.retriever = self._prepare_retriever()
        
        self.fix_prompt = PromptTemplate.from_template(
            "### Instructions:\nFix the DuckDB SQL based on the error. Return ONLY SQL.\n"
            "### Schema:\n{schema}\n### Error:\n{error}\n### Faulty SQL:\n{sql}\n### Response:"
        )
    def bind_dataframe(self,df,table_name):
        self.table_name =table_name
        self.con = duckdb.connect(database=":memory:")
        self.con.register(self.table_name, df)
        self.retriever = self._prepare_retriever()

    def _prepare_retriever(self):
        schema_df = self.con.execute(f"DESCRIBE {self.table_name}").fetchdf()
        schema_text = f"Table: {self.table_name}\nColumns:\n"
        for _, row in schema_df.iterrows():
            schema_text += f"- {row['column_name']} ({row['column_type']})\n"
        
        sample_text = self.con.execute(f"SELECT * FROM {self.table_name} LIMIT 3").fetchdf().to_markdown()
        
        doc = Document(page_content=f"{schema_text}\n\nSample:\n{sample_text}")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"}
        )
        vectorstore = Chroma.from_documents([doc], embedding=embeddings)
        return vectorstore.as_retriever(search_kwargs={"k": 1})

    def _validate_sql(self, sql):
        """Checks for both security (regex) and syntax (sqlglot)."""
        sql_clean = sql.strip().lower()
        
        # 1. Security Check: Block destructive keywords
        forbidden = ["drop", "delete", "update", "insert", "alter", "truncate"]
        if not sql_clean.startswith("select") or any(re.search(rf"\b{kw}\b", sql_clean) for kw in forbidden):
            return False, "Query is either non-SELECT or contains forbidden keywords."

        # 2. Syntax Check: Use sqlglot to parse for DuckDB dialect
        try:
            # This attempts to parse the SQL; if it's gibberish, it raises ParseError
            parsed = sqlglot.transpile(
                                    sql,
                                    read="duckdb",
                                    write="duckdb",
                                    pretty=True
                                )[0]
            if not parsed:
                raise sqlglot.errors.ParseError("Empty SQL after transpile")

            return True, None
        except sqlglot.errors.ParseError as e:
            return False, f"SQL Syntax Error: {str(e)}"

    def get_result(self, question, max_retries=3):
        context = self.retriever.invoke(question)[0].page_content
        
        prompt = f"""### Instructions:Generate DuckDB SQL.
- Use the provided schema only.
- Use Table Aliases.
- Do NOT add explanations.
- Do NOT hallucinate columns.
- Return ONLY the SQL.
### Schema:{context}
### Question:{question}
### Response:"""
        
        current_sql = generate_sql(prompt)

        for attempt in range(max_retries + 1):
            # STEP 1: Validation with sqlglot and security check
            is_valid, validation_error = self._validate_sql(current_sql)
            
            if not is_valid:
                print(f"⚠️ Validation Failed (Attempt {attempt+1}): {validation_error}")
                if attempt == max_retries:
                    return f"Error: Final SQL failed validation: {validation_error}"
                
                # Treat validation error as a query error to trigger the fix loop
                fix_msg = self.fix_prompt.format(schema=context, error=validation_error, sql=current_sql)
                current_sql = generate_sql(fix_msg)
                continue

            # STEP 2: Execution in DuckDB
            try:
                df_result = self.con.execute(current_sql).fetchdf()
                self.history.append({"q": question, "sql": current_sql})
                if len(self.history) > self.max_history: self.history.pop(0)
                
                return {"sql": current_sql, "data": df_result}

            except Exception as e:
                print(f"❌ Execution Error (Attempt {attempt+1}): {str(e)}")
                if attempt == max_retries:
                    return f"Error: Failed after retries. Last error: {str(e)}"
                
                fix_msg = self.fix_prompt.format(schema=context, error=str(e), sql=current_sql)
                current_sql = generate_sql(fix_msg)