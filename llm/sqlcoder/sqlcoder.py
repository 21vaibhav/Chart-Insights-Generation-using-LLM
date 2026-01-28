# import pandas as pd
# import duckdb
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_core.documents import Document
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# from langchain_community.llms import HuggingFacePipeline
# import torch
# from sqlcoder_loader import generate_sql



# def make_connection(df:pd.DataFrame,file_name):
#     con = duckdb.connect(database=":memory:")
#     con.register(file_name,df)
#     return con 


# def sql_check(con,query):
#     return con.execute(query).fetchdf()


# def get_schema(con,table_name):
#     return con.execute(f"DESCRIBE {table_name}").fetchdf()


# def schema_to_text(table_name, con):
#     df = get_schema(con,table_name)
#     text = f"Table: {table_name}\nColumns:\n"
#     for _, row in df.iterrows():
#         text += f"- {row['column_name']} ({row['column_type']})\n"
#     return text


# def get_sample(con,table_name):
#     sample_df = con.execute(f"select * from {table_name} limit 5").fetchdf()
#     sample_text = sample_df.to_markdown(index=False)
#     return sample_text


# def schema_doc(table_name,schema_text,sample_text):
#     docs = [Document(page_content=f"""
# {schema_text}

# Sample rows:
# {sample_text}     
# """,metadata={'table':table_name})]
#     return docs
    

# def generate_embeddings(docs):
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",model_kwargs={"device": "cuda"})
#     vectorstore = Chroma.from_documents(docs,embedding=embeddings,collection_name="telemetry_schema",)
#     retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
#     return retriever

# def get_schema_context(retriever,question):
#     docs = retriever.invoke(question)
#     return "\n".join(d.page_content for d in docs)
    

# def ask_sqlcoder(user_question, retriever):
#     # 1. Get the schema context (Table DDL + Sample Rows) from your vector store
#     context = get_schema_context(retriever, user_question)
    
#     # 2. Use the "Official" SQLCoder format
#     # It works best with specific headers: Instructions, Input, Response
#     full_prompt = f"""### Instructions:
# Your task is to convert a question into a DuckDB SQL query, given a database schema.
# Adhere to these rules:
# - **Use the provided schema only.**
# - **Use Table Aliases** to prevent ambiguity (e.g., telemetry.temp).
# - **Return ONLY the SQL** and nothing else.
# - If you cannot answer the question, say "sorry!".

# ### Input:
# Generate a DuckDB SQL query that answers the question: `{user_question}`.

# This query will run on a database with the following schema:
# {context}

# ### Response:
# """
#     return generate_sql(full_prompt)


# def sql_results(con,query):

#     return con.execute(query).fetchdf()



# if __name__ == "__main__":
#     df = pd.read_csv(r"C:\Users\Dell\OneDrive\Desktop\project_2026\telemetry_data.csv")
#     df['StartDateUTC'] = pd.to_datetime(df['StartDateUTC'])
#     df['EndDateUTC'] =  pd.to_datetime(df['EndDateUTC'])
#     con = make_connection(df,'telemetry')
#     print(sql_check(con,"select * from telemetry"))
#     print(get_schema(con,'telemetry'))
#     schema_text = schema_to_text("telemetry", con)
#     print(schema_text)
#     sample_text = get_sample(con,"telemetry")
#     print(sample_text)
#     docs = schema_doc('telemetry',schema_text,sample_text)
#     print(docs)
#     retriver = generate_embeddings(docs)
#     context = get_schema_context(retriver,"telemetry schema")
#     result = ask_sqlcoder(user_question="what are the unique draft not present in the first 6 months and appeared later? ",retriever=retriver)
#     print(result)
#     print(sql_results(con,result))
    
    
    



import pandas as pd
from sql_manager import SQLQueryManager

# 1. Setup Data
df = pd.read_csv(r"C:\Users\Dell\OneDrive\Desktop\project_2026\telemetry_data.csv")
df['StartDateUTC'] = pd.to_datetime(df['StartDateUTC'])
df['EndDateUTC'] =  pd.to_datetime(df['EndDateUTC'])

# 2. Initialize Manager
manager = SQLQueryManager()

def run_app():
    while True:
        query = input("\nAsk your data a question (or 'exit'): ")
        if query.lower() == 'exit': break
        
        # 3. Simple One-Line Call
        manager.bind_dataframe(df,'telemetry')
        response = manager.get_result(query)
        
        if isinstance(response, dict):
            print(f"\n[SQL]: {response['sql']}")
            print("\n[Data]:")
            print(response['data'])
        else:
            print(f"\n[System]: {response}")

if __name__ == "__main__":
    run_app()
    