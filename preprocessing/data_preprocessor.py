# preprocess/data_preprocessor.py

import pandas as pd
from typing import Dict, Any


# -------------------------------------------------
# 2️⃣ BASIC PREPROCESSING
# -------------------------------------------------
def preprocess_dataframe(
    df: pd.DataFrame,
    drop_duplicates: bool = True,
    drop_nulls: bool = False,
    fill_missing: bool = False
) -> pd.DataFrame:
    """
    Apply safe preprocessing steps
    """

    df = df.copy()

    # Drop duplicate rows
    if drop_duplicates:
        df = df.drop_duplicates()

    # Drop rows with ANY null values
    if drop_nulls:
        df = df.dropna()

    # Optional missing value filling
    if fill_missing and not drop_nulls:
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna("Unknown")

    return df


# -------------------------------------------------
# 3️⃣ DATAFRAME SCHEMA INFO (df.info-like)
# -------------------------------------------------
def get_dataframe_info(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Structured version of df.info()
    Schema-level metadata ONLY
    """

    schema = {
        "num_rows": int(df.shape[0]),
        "num_columns": int(df.shape[1]),
        "columns": []
    }

    for col in df.columns:
        col_schema = {
            "column_name": col,
            "dtype": str(df[col].dtype),
            "non_null_count": int(df[col].notnull().sum()),
            "null_count": int(df[col].isnull().sum())
        }

        schema["columns"].append(col_schema)

    return schema


# -------------------------------------------------
# 4️⃣ DATAFRAME SUMMARY (df.describe-like)
# -------------------------------------------------
def get_dataframe_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Structured statistical summary (df.describe equivalent)
    """

    summary = {}

    describe_df = df.describe(include="all").fillna("")

    for col in describe_df.columns:
        col_stats = {}

        for stat in describe_df.index:
            value = describe_df.loc[stat, col]

            if isinstance(value, (int, float)):
                col_stats[stat] = float(value)
            else:
                col_stats[stat] = str(value)

        summary[col] = col_stats

    return summary


# -------------------------------------------------
# 5️⃣ OPTIONAL SMART HELPERS
# -------------------------------------------------
def detect_datetime_columns(df: pd.DataFrame) -> list:
    """
    Detect potential datetime columns
    """

    datetime_cols = []
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                pd.to_datetime(df[col])
                datetime_cols.append(col)
            except Exception:
                pass

    return datetime_cols


# def detect_categorical_columns(df: pd.DataFrame, threshold: int = 20) -> list:
#     """
#     Detect categorical columns based on unique count
#     """

#     categorical_cols = []
#     for col in df.columns:
#         if df[col].nunique() <= threshold:
#             categorical_cols.append(col)

#     return categorical_cols
