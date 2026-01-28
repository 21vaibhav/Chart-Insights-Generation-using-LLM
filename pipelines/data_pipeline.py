import pandas as pd
from typing import Dict, Any, Tuple

from preprocessing.data_preprocessor import (
    preprocess_dataframe,
    get_dataframe_info,
    get_dataframe_summary,
)


def run_data_pipeline(
    df: pd.DataFrame,
    drop_duplicates: bool = True,
    drop_nulls: bool = False,
    fill_missing: bool = False,
) -> Tuple[pd.DataFrame, Dict[str, Any], Dict[str, Any]]:
    """
    Core data processing pipeline

    Steps:
    1. Preprocess dataframe
    2. Extract schema info
    3. Extract statistical summary

    Returns:
    - preprocessed_df
    - schema_info
    - data_summary
    """

    if df is None or df.empty:
        raise ValueError("Input dataframe is empty or None")

    # -----------------------------
    # 1️⃣ PREPROCESS
    # -----------------------------
    processed_df = preprocess_dataframe(
        df=df,
        drop_duplicates=drop_duplicates,
        drop_nulls=drop_nulls,
        fill_missing=fill_missing,
    )

    # -----------------------------
    # 2️⃣ SCHEMA INFO
    # -----------------------------
    schema_info = get_dataframe_info(processed_df)

    # -----------------------------
    # 3️⃣ DATA SUMMARY
    # -----------------------------
    data_summary = get_dataframe_summary(processed_df)

    return processed_df

    return processed_df, schema_info, data_summary

