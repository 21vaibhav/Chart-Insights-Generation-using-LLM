from pandas import DataFrame
from pipelines.data_pipeline import run_data_pipeline
from preprocessing.query_preprocessor import query_parse_lower


def df_query(df:DataFrame,query:str):
    df  = run_data_pipeline(df)
    query = query_parse_lower(query)
    return df,query